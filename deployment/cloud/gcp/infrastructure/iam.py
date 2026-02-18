"""Service accounts and IAM role bindings."""

from dataclasses import dataclass

import pulumi_gcp as gcp

from config import GCP_PROJECT


@dataclass
class IAMResources:
    service_accounts: dict


# Service account definitions: (logical_name, account_id, display_name, roles)
SA_DEFINITIONS = [
    (
        "webservice",
        "biocirv-staging-cr-websvc",
        "Webservice Cloud Run SA",
        ["roles/cloudsql.client", "roles/secretmanager.secretAccessor"],
    ),
    (
        "prefect-server",
        "biocirv-staging-cr-prefect",
        "Prefect Server Cloud Run SA",
        ["roles/cloudsql.client"],
    ),
    (
        "prefect-worker",
        "biocirv-staging-cr-worker",
        "Prefect Worker Cloud Run SA",
        ["roles/cloudsql.client", "roles/run.admin", "roles/iam.serviceAccountUser"],
    ),
    (
        "flowrun",
        "biocirv-staging-cr-flowrun",
        "Flow Run Cloud Run SA",
        ["roles/cloudsql.client", "roles/secretmanager.secretAccessor"],
    ),
    (
        "migrate",
        "biocirv-staging-cr-migrate",
        "Migration Cloud Run SA",
        ["roles/cloudsql.client", "roles/secretmanager.secretAccessor"],
    ),
]


def create_service_accounts() -> IAMResources:
    """Create service accounts and IAM role bindings."""
    service_accounts = {}

    for logical_name, account_id, display_name, roles in SA_DEFINITIONS:
        sa = gcp.serviceaccount.Account(
            f"sa-{logical_name}",
            account_id=account_id,
            display_name=display_name,
        )
        service_accounts[logical_name] = sa

        for role in roles:
            role_short = role.split("/")[-1]
            gcp.projects.IAMMember(
                f"sa-{logical_name}-{role_short}",
                project=GCP_PROJECT,
                role=role,
                member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
            )

    return IAMResources(service_accounts=service_accounts)
