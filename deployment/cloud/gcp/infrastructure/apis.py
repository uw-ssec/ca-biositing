"""Enable required GCP APIs."""

import pulumi_gcp as gcp

REQUIRED_APIS = [
    "sqladmin.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "artifactregistry.googleapis.com",  # gcr.io uses AR as backend
    "cloudbuild.googleapis.com",
]


def enable_apis():
    """Enable GCP APIs needed by the infrastructure."""
    services = {}
    for api in REQUIRED_APIS:
        name = api.split(".")[0]
        services[name] = gcp.projects.Service(
            f"api-{name}",
            service=api,
            disable_on_destroy=False,
        )
    return services
