"""Cloud Router and Cloud NAT for VPC egress from Cloud Run."""

from dataclasses import dataclass
from typing import Sequence

import pulumi
import pulumi_gcp as gcp

from config import GCP_REGION, STACK_NAME


@dataclass
class NetworkingResources:
    router: gcp.compute.Router
    nat: gcp.compute.RouterNat


def create_cloud_nat(
    depends_on: Sequence[pulumi.Resource] | None = None,
) -> NetworkingResources:
    """Create Cloud Router + Cloud NAT on the default VPC.

    This enables Cloud Run services with Direct VPC egress
    (egress=ALL_TRAFFIC) to reach external endpoints (e.g. Google OAuth APIs)
    while still routing traffic through the VPC for internal ingress.
    """
    opts = pulumi.ResourceOptions(depends_on=depends_on or [])

    router = gcp.compute.Router(
        "cloud-router",
        name=f"biocirv-{STACK_NAME}-router",
        region=GCP_REGION,
        network="default",
        opts=opts,
    )

    nat = gcp.compute.RouterNat(
        "cloud-nat",
        name=f"biocirv-{STACK_NAME}-nat",
        router=router.name,
        region=GCP_REGION,
        nat_ip_allocate_option="AUTO_ONLY",
        source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
        opts=pulumi.ResourceOptions(depends_on=[router]),
    )

    return NetworkingResources(router=router, nat=nat)
