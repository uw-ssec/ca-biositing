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

# GitHub repository (org/repo) for Workload Identity Federation
GITHUB_REPO = "sustainability-software-lab/ca-biositing"

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
GHCR_BASE = "ghcr.io/sustainability-software-lab/ca-biositing"
IMAGE_TAG = os.environ.get("IMAGE_TAG", "latest")
WEBSERVICE_IMAGE = os.environ.get(
    "WEBSERVICE_IMAGE", f"{GHCR_BASE}/webservice:{IMAGE_TAG}"
)
PIPELINE_IMAGE = os.environ.get(
    "PIPELINE_IMAGE", f"{GHCR_BASE}/pipeline:{IMAGE_TAG}"
)
PREFECT_SERVER_IMAGE = os.environ.get(
    "PREFECT_SERVER_IMAGE", "prefecthq/prefect:3-python3.12"
)

# LandIQ shapefile URL for Cloud Run (2023 provisional crop mapping dataset)
LANDIQ_SHAPEFILE_URL = os.environ.get(
    "LANDIQ_SHAPEFILE_URL",
    "https://data.cnra.ca.gov/dataset/6c3d65e3-35bb-49e1-a51e-49d5a2cf09a9/resource/25d0f174-4bec-4987-a402-602cd1372786/download/i15_crop_mapping_2023_provisional.zip",
)


def configure_stack(stack: auto.Stack) -> None:
    """Set all stack configuration programmatically."""
    stack.set_config("gcp:project", auto.ConfigValue(GCP_PROJECT))
    stack.set_config("gcp:region", auto.ConfigValue(GCP_REGION))
