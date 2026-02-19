"""Cloud SQL instance, databases, and users."""

from dataclasses import dataclass

import pulumi_gcp as gcp

from config import (
    GCP_REGION,
    DB_INSTANCE_NAME,
    DB_NAME,
    PREFECT_DB_NAME,
)


@dataclass
class CloudSQLResources:
    instance: gcp.sql.DatabaseInstance
    database: gcp.sql.Database
    prefect_database: gcp.sql.Database


def create_cloud_sql() -> CloudSQLResources:
    """Create Cloud SQL instance with databases."""
    instance = gcp.sql.DatabaseInstance(
        "staging-db-instance",
        name=DB_INSTANCE_NAME,
        database_version="POSTGRES_17",
        region=GCP_REGION,
        deletion_protection=True,
        settings=gcp.sql.DatabaseInstanceSettingsArgs(
            tier="db-custom-2-8192",
            edition="ENTERPRISE",
            availability_type="ZONAL",
            ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
                ipv4_enabled=True,
                ssl_mode="ENCRYPTED_ONLY",
            ),
            backup_configuration=gcp.sql.DatabaseInstanceSettingsBackupConfigurationArgs(
                enabled=True,
                start_time="03:00",
                backup_retention_settings=gcp.sql.DatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsArgs(
                    retained_backups=7,
                ),
                point_in_time_recovery_enabled=True,
                transaction_log_retention_days=3,
            ),
            maintenance_window=gcp.sql.DatabaseInstanceSettingsMaintenanceWindowArgs(
                day=7,  # Sunday
                hour=4,
                update_track="stable",
            ),
            insights_config=gcp.sql.DatabaseInstanceSettingsInsightsConfigArgs(
                query_insights_enabled=True,
            ),
        ),
    )

    database = gcp.sql.Database(
        "staging-db",
        name=DB_NAME,
        instance=instance.name,
    )

    prefect_database = gcp.sql.Database(
        "prefect-db",
        name=PREFECT_DB_NAME,
        instance=instance.name,
    )

    return CloudSQLResources(
        instance=instance,
        database=database,
        prefect_database=prefect_database,
    )
