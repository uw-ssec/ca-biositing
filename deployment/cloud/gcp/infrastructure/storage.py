"""GCS Bucket resources."""

from dataclasses import dataclass
from typing import Sequence

import pulumi
import pulumi_gcp as gcp

from config import IMAGE_BUCKET_NAME, GCP_REGION


@dataclass
class StorageResources:
    bucket: gcp.storage.Bucket


def create_storage_resources(
    depends_on: Sequence[pulumi.Resource] | None = None,
) -> StorageResources:
    """Create GCS buckets."""
    opts = pulumi.ResourceOptions(depends_on=depends_on or [])

    # Create the image bucket
    bucket = gcp.storage.Bucket(
        "image-bucket",
        name=IMAGE_BUCKET_NAME,
        location=GCP_REGION,
        uniform_bucket_level_access=True,
        force_destroy=False,  # Protect images from accidental deletion
        opts=opts,
    )

    # Make the bucket public (read-only) for the data portal
    gcp.storage.BucketIAMMember(
        "image-bucket-public-viewer",
        bucket=bucket.name,
        role="roles/storage.objectViewer",
        member="allUsers",
    )

    return StorageResources(bucket=bucket)
