"""Artifact Registry remote repository for proxying GHCR and Quay.io images.

These repositories are project-level (not environment-specific) and shared
across all Pulumi stacks.  The staging stack creates them; other stacks import
the existing resources via ``import_`` so Pulumi adopts rather than re-creates.
``retain_on_delete`` prevents accidental deletion when any single stack is torn
down.
"""

import pulumi
import pulumi_gcp as gcp

from config import GCP_PROJECT, GCP_REGION, STACK_NAME

# GCP resource path for AR repos — used to import existing shared repos.
_AR_PATH_PREFIX = f"projects/{GCP_PROJECT}/locations/{GCP_REGION}/repositories"


def create_artifact_registry(depends_on=None):
    """Create an AR remote repository that proxies GHCR.

    Cloud Run only accepts images from gcr.io, docker.pkg.dev, or docker.io.
    This remote repo lets Cloud Run pull GHCR images via AR transparently.
    """
    opts_kwargs = dict(
        depends_on=depends_on or [],
        delete_before_replace=True,
        retain_on_delete=True,
    )
    if STACK_NAME != "staging":
        opts_kwargs["import_"] = f"{_AR_PATH_PREFIX}/ghcr-proxy"

    repo = gcp.artifactregistry.Repository(
        "ghcr-proxy",
        repository_id="ghcr-proxy",
        location=GCP_REGION,
        format="DOCKER",
        mode="REMOTE_REPOSITORY",
        remote_repository_config=gcp.artifactregistry.RepositoryRemoteRepositoryConfigArgs(
            docker_repository=gcp.artifactregistry.RepositoryRemoteRepositoryConfigDockerRepositoryArgs(
                custom_repository=gcp.artifactregistry.RepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryArgs(
                    uri="https://ghcr.io",
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(**opts_kwargs),
    )
    return repo


def create_quayio_registry(depends_on=None):
    """Create an AR remote repository that proxies Quay.io.

    Cloud Run only accepts images from gcr.io, docker.pkg.dev, or docker.io.
    This remote repo lets Cloud Run pull Quay.io images (e.g., oauth2-proxy) via AR.
    """
    opts_kwargs = dict(
        depends_on=depends_on or [],
        delete_before_replace=True,
        retain_on_delete=True,
    )
    if STACK_NAME != "staging":
        opts_kwargs["import_"] = f"{_AR_PATH_PREFIX}/quayio-proxy"

    repo = gcp.artifactregistry.Repository(
        "quayio-proxy",
        repository_id="quayio-proxy",
        location=GCP_REGION,
        format="DOCKER",
        mode="REMOTE_REPOSITORY",
        remote_repository_config=gcp.artifactregistry.RepositoryRemoteRepositoryConfigArgs(
            docker_repository=gcp.artifactregistry.RepositoryRemoteRepositoryConfigDockerRepositoryArgs(
                custom_repository=gcp.artifactregistry.RepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryArgs(
                    uri="https://quay.io",
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(**opts_kwargs),
    )
    return repo
