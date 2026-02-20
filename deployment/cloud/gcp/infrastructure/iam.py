"""Service accounts and IAM role bindings."""

from dataclasses import dataclass
from typing import Sequence

import pulumi
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
        [
            "roles/cloudsql.client",
            "roles/secretmanager.secretAccessor",
            "roles/artifactregistry.reader",
        ],
    ),
    (
        "prefect-server",
        "biocirv-staging-cr-prefect",
        "Prefect Server Cloud Run SA",
        [
            "roles/cloudsql.client",
            "roles/secretmanager.secretAccessor",
        ],
    ),
    (
        "prefect-worker",
        "biocirv-staging-cr-worker",
        "Prefect Worker Cloud Run SA",
        [
            "roles/cloudsql.client",
            "roles/secretmanager.secretAccessor",
            "roles/artifactregistry.reader",
        ],
    ),
    (
        "migrate",
        "biocirv-staging-cr-migrate",
        "Migration Cloud Run SA",
        [
            "roles/cloudsql.client",
            "roles/secretmanager.secretAccessor",
            "roles/artifactregistry.reader",
        ],
    ),
]


def create_service_accounts(
    depends_on: Sequence[pulumi.Resource] | None = None,
) -> IAMResources:
    """Create service accounts and IAM role bindings."""
    service_accounts = {}
    opts = pulumi.ResourceOptions(depends_on=depends_on or [])

    for logical_name, account_id, display_name, roles in SA_DEFINITIONS:
        sa = gcp.serviceaccount.Account(
            f"sa-{logical_name}",
            account_id=account_id,
            display_name=display_name,
            opts=opts,
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
