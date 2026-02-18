"""Stack configuration and project constants."""

from pulumi import automation as auto

# Project and stack settings
PROJECT_NAME = "ca-biositing-infrastructure"
STACK_NAME = "staging"
BACKEND_URL = "gs://biocirv-470318-pulumi-state"

# GCP settings
GCP_PROJECT = "biocirv-470318"
GCP_REGION = "us-west1"

# Cloud SQL
DB_INSTANCE_NAME = "biocirv-staging"
DB_NAME = "biocirv-staging"
PREFECT_DB_NAME = "prefect"
DB_USER = "biocirv_user"

# Read-only users
READONLY_USERS = ["biocirv_readonly"]

# Container images (GCR for custom images; Docker Hub for official images)
GCR_BASE = f"gcr.io/{GCP_PROJECT}"
WEBSERVICE_IMAGE = f"{GCR_BASE}/webservice:latest"
PIPELINE_IMAGE = f"{GCR_BASE}/pipeline:latest"
PREFECT_WORKER_IMAGE = f"{GCR_BASE}/prefect-worker:latest"
PREFECT_SERVER_IMAGE = "prefecthq/prefect:3-python3.12"


def configure_stack(stack: auto.Stack) -> None:
    """Set all stack configuration programmatically."""
    stack.set_config("gcp:project", auto.ConfigValue(GCP_PROJECT))
    stack.set_config("gcp:region", auto.ConfigValue(GCP_REGION))
