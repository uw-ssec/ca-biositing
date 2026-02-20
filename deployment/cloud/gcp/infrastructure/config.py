"""Stack configuration and project constants."""

import os

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
PREFECT_WORK_POOL_NAME = "biocirv-staging-pool"
DB_USER = "biocirv_user"

# Read-only users
READONLY_USERS = ["biocirv_readonly"]

# Container images — override with env vars to use digest/commit-based tags
# instead of :latest (which Pulumi cannot detect changes for).
GCR_BASE = f"gcr.io/{GCP_PROJECT}"
IMAGE_TAG = os.environ.get("IMAGE_TAG", "latest")
WEBSERVICE_IMAGE = os.environ.get(
    "WEBSERVICE_IMAGE", f"{GCR_BASE}/webservice:{IMAGE_TAG}"
)
PIPELINE_IMAGE = os.environ.get(
    "PIPELINE_IMAGE", f"{GCR_BASE}/pipeline:{IMAGE_TAG}"
)
PREFECT_SERVER_IMAGE = os.environ.get(
    "PREFECT_SERVER_IMAGE", "prefecthq/prefect:3-python3.12"
)


def configure_stack(stack: auto.Stack) -> None:
    """Set all stack configuration programmatically."""
    stack.set_config("gcp:project", auto.ConfigValue(GCP_PROJECT))
    stack.set_config("gcp:region", auto.ConfigValue(GCP_REGION))
