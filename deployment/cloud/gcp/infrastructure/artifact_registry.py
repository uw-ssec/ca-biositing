"""Artifact Registry remote repository for proxying GHCR and Quay.io images."""

import pulumi
import pulumi_gcp as gcp

from config import GCP_REGION


def create_artifact_registry(depends_on=None):
    """Create an AR remote repository that proxies GHCR.

    Cloud Run only accepts images from gcr.io, docker.pkg.dev, or docker.io.
    This remote repo lets Cloud Run pull GHCR images via AR transparently.
    """
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
        opts=pulumi.ResourceOptions(
            depends_on=depends_on or [],
            delete_before_replace=True,
        ),
    )
    return repo


def create_quayio_registry(depends_on=None):
    """Create an AR remote repository that proxies Quay.io.

    Cloud Run only accepts images from gcr.io, docker.pkg.dev, or docker.io.
    This remote repo lets Cloud Run pull Quay.io images (e.g., oauth2-proxy) via AR.
    """
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
        opts=pulumi.ResourceOptions(
            depends_on=depends_on or [],
            delete_before_replace=True,
        ),
    )
    return repo
