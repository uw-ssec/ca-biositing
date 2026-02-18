"""Cloud Run Services and Jobs."""

from dataclasses import dataclass

import pulumi
import pulumi_gcp as gcp

from config import (
    GCP_REGION,
    WEBSERVICE_IMAGE,
    PIPELINE_IMAGE,
    PREFECT_WORKER_IMAGE,
    PREFECT_SERVER_IMAGE,
    DB_USER,
    DB_NAME,
    PREFECT_DB_NAME,
)
from cloud_sql import CloudSQLResources
from secrets import SecretResources
from iam import IAMResources


@dataclass
class CloudRunResources:
    webservice: gcp.cloudrunv2.Service
    migration_job: gcp.cloudrunv2.Job
    prefect_server: gcp.cloudrunv2.Service
    prefect_worker: gcp.cloudrunv2.Service


def create_cloud_run_resources(
    sql: CloudSQLResources,
    secrets: SecretResources,
    iam: IAMResources,
) -> CloudRunResources:
    """Create all Cloud Run Services and Jobs."""

    # --- 5.2: FastAPI Webservice ---
    webservice = gcp.cloudrunv2.Service(
        "webservice",
        name="biocirv-webservice",
        location=GCP_REGION,
        ingress="INGRESS_TRAFFIC_ALL",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=iam.service_accounts["webservice"].email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=1,
                max_instance_count=10,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=WEBSERVICE_IMAGE,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "512Mi"},
                        cpu_idle=False,
                        startup_cpu_boost=True,
                    ),
                    envs=[
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="DB_USER",
                            value=DB_USER,
                        ),
                        # App config uses POSTGRES_DB when INSTANCE_CONNECTION_NAME is set
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="POSTGRES_DB",
                            value=DB_NAME,
                        ),
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="DB_PASS",
                            value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
                                secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                                    secret=secrets.db_password_secret.secret_id,
                                    version="latest",
                                )
                            ),
                        ),
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="INSTANCE_CONNECTION_NAME",
                            value=sql.instance.connection_name,
                        ),
                    ],
                    volume_mounts=[
                        gcp.cloudrunv2.ServiceTemplateContainerVolumeMountArgs(
                            name="cloudsql",
                            mount_path="/cloudsql",
                        )
                    ],
                    startup_probe=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeArgs(
                        tcp_socket=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeTcpSocketArgs(
                            port=8080,
                        ),
                    ),
                    liveness_probe=gcp.cloudrunv2.ServiceTemplateContainerLivenessProbeArgs(
                        http_get=gcp.cloudrunv2.ServiceTemplateContainerLivenessProbeHttpGetArgs(
                            path="/",
                            port=8080,
                        ),
                    ),
                )
            ],
            volumes=[
                gcp.cloudrunv2.ServiceTemplateVolumeArgs(
                    name="cloudsql",
                    cloud_sql_instance=gcp.cloudrunv2.ServiceTemplateVolumeCloudSqlInstanceArgs(
                        instances=[sql.instance.connection_name],
                    ),
                )
            ],
        ),
        traffics=[
            gcp.cloudrunv2.ServiceTrafficArgs(
                type="TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
                percent=100,
            )
        ],
    )

    gcp.cloudrunv2.ServiceIamMember(
        "webservice-public-access",
        name=webservice.name,
        location=GCP_REGION,
        role="roles/run.invoker",
        member="allUsers",
    )

    # --- 5.3: Alembic Migration Job ---
    database_url = pulumi.Output.all(
        password=secrets.db_password.result,
        connection_name=sql.instance.connection_name,
    ).apply(
        lambda args: (
            f"postgresql+psycopg2://{DB_USER}:{args['password']}"
            f"@/{DB_NAME}?host=/cloudsql/{args['connection_name']}"
        )
    )

    migration_job = gcp.cloudrunv2.Job(
        "migration-job",
        name="biocirv-alembic-migrate",
        location=GCP_REGION,
        template=gcp.cloudrunv2.JobTemplateArgs(
            template=gcp.cloudrunv2.JobTemplateTemplateArgs(
                max_retries=1,
                timeout="600s",
                service_account=iam.service_accounts["migrate"].email,
                containers=[
                    gcp.cloudrunv2.JobTemplateTemplateContainerArgs(
                        image=PIPELINE_IMAGE,
                        commands=["alembic", "upgrade", "head"],
                        resources=gcp.cloudrunv2.JobTemplateTemplateContainerResourcesArgs(
                            limits={"cpu": "1", "memory": "512Mi"},
                        ),
                        envs=[
                            gcp.cloudrunv2.JobTemplateTemplateContainerEnvArgs(
                                name="DATABASE_URL",
                                value=database_url,
                            ),
                        ],
                        volume_mounts=[
                            gcp.cloudrunv2.JobTemplateTemplateContainerVolumeMountArgs(
                                name="cloudsql",
                                mount_path="/cloudsql",
                            )
                        ],
                    )
                ],
                volumes=[
                    gcp.cloudrunv2.JobTemplateTemplateVolumeArgs(
                        name="cloudsql",
                        cloud_sql_instance=gcp.cloudrunv2.JobTemplateTemplateVolumeCloudSqlInstanceArgs(
                            instances=[sql.instance.connection_name],
                        ),
                    )
                ],
            )
        ),
    )

    # --- 5.4: Self-hosted Prefect Server ---
    prefect_db_url = pulumi.Output.all(
        password=secrets.db_password.result,
        connection_name=sql.instance.connection_name,
    ).apply(
        lambda args: (
            f"postgresql+asyncpg://{DB_USER}:{args['password']}"
            f"@/{PREFECT_DB_NAME}?host=/cloudsql/{args['connection_name']}"
        )
    )

    prefect_server = gcp.cloudrunv2.Service(
        "prefect-server",
        name="biocirv-prefect-server",
        location=GCP_REGION,
        ingress="INGRESS_TRAFFIC_ALL",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=iam.service_accounts["prefect-server"].email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=1,
                max_instance_count=1,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=PREFECT_SERVER_IMAGE,
                    commands=[
                        "prefect",
                        "server",
                        "start",
                        "--host",
                        "0.0.0.0",
                        "--port",
                        "4200",
                    ],
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=4200,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "1Gi"},
                    ),
                    envs=[
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="PREFECT_API_DATABASE_CONNECTION_URL",
                            value=prefect_db_url,
                        ),
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="PREFECT_SERVER_API_HOST",
                            value="0.0.0.0",
                        ),
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="PREFECT_SERVER_API_PORT",
                            value="4200",
                        ),
                    ],
                    volume_mounts=[
                        gcp.cloudrunv2.ServiceTemplateContainerVolumeMountArgs(
                            name="cloudsql",
                            mount_path="/cloudsql",
                        )
                    ],
                    startup_probe=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeArgs(
                        http_get=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeHttpGetArgs(
                            path="/api/health",
                            port=4200,
                        ),
                        initial_delay_seconds=30,
                        period_seconds=10,
                        failure_threshold=10,
                    ),
                    liveness_probe=gcp.cloudrunv2.ServiceTemplateContainerLivenessProbeArgs(
                        http_get=gcp.cloudrunv2.ServiceTemplateContainerLivenessProbeHttpGetArgs(
                            path="/api/health",
                            port=4200,
                        ),
                    ),
                )
            ],
            volumes=[
                gcp.cloudrunv2.ServiceTemplateVolumeArgs(
                    name="cloudsql",
                    cloud_sql_instance=gcp.cloudrunv2.ServiceTemplateVolumeCloudSqlInstanceArgs(
                        instances=[sql.instance.connection_name],
                    ),
                )
            ],
        ),
        traffics=[
            gcp.cloudrunv2.ServiceTrafficArgs(
                type="TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
                percent=100,
            )
        ],
    )

    gcp.cloudrunv2.ServiceIamMember(
        "prefect-server-public-access",
        name=prefect_server.name,
        location=GCP_REGION,
        role="roles/run.invoker",
        member="allUsers",
    )

    # --- 5.5: Prefect Worker ---
    prefect_api_url = prefect_server.uri.apply(lambda uri: f"{uri}/api")

    prefect_worker = gcp.cloudrunv2.Service(
        "prefect-worker",
        name="biocirv-prefect-worker",
        location=GCP_REGION,
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=iam.service_accounts["prefect-worker"].email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=0,
                max_instance_count=1,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=PREFECT_WORKER_IMAGE,
                    commands=[
                        "prefect",
                        "worker",
                        "start",
                        "--pool",
                        "biocirv-staging-pool",
                        "--type",
                        "cloud-run-v2",
                        "--with-healthcheck",
                    ],
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "512Mi"},
                    ),
                    envs=[
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="PREFECT_API_URL",
                            value=prefect_api_url,
                        ),
                        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                            name="CLOUDSQL_CONNECTION_NAME",
                            value=sql.instance.connection_name,
                        ),
                    ],
                    startup_probe=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeArgs(
                        tcp_socket=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeTcpSocketArgs(
                            port=8080,
                        ),
                        initial_delay_seconds=15,
                        period_seconds=10,
                        failure_threshold=30,
                    ),
                )
            ],
        ),
        traffics=[
            gcp.cloudrunv2.ServiceTrafficArgs(
                type="TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
                percent=100,
            )
        ],
    )

    return CloudRunResources(
        webservice=webservice,
        migration_job=migration_job,
        prefect_server=prefect_server,
        prefect_worker=prefect_worker,
    )
