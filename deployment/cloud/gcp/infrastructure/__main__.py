"""GCP infrastructure for ca-biositing staging environment."""

import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
project_id = config.get("project_id") or "biocirv-470318"
region = config.get("region") or "us-west1"

# Cloud SQL instance for staging environment
staging_db_instance = gcp.sql.DatabaseInstance(
    "staging-db-instance",
    name="biocirv-staging",
    database_version="POSTGRES_17",
    region=region,
    deletion_protection=True,
    settings=gcp.sql.DatabaseInstanceSettingsArgs(
        tier="db-custom-2-8192",
        edition="ENTERPRISE",
    ),
)

# Database within the staging Cloud SQL instance
staging_db = gcp.sql.Database(
    "staging-db",
    name="biocirv-staging",
    instance=staging_db_instance.name,
)

# Exports
pulumi.export("db_instance_name", staging_db_instance.name)
pulumi.export("database_name", staging_db.name)
