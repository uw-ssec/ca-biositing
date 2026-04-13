"""Cloud Router and Cloud NAT for VPC egress from Cloud Run.

Cloud NAT with ``ALL_SUBNETWORKS_ALL_IP_RANGES`` is a per-VPC/region singleton
in GCP.  The router and NAT are shared across all environments in the same
project/VPC, so they use environment-neutral names (``biocirv-router``,
``biocirv-nat``).  Every Pulumi stack imports these shared resources with
``retain_on_delete`` so that tearing down one stack does not break egress for
others.
"""

from dataclasses import dataclass
from typing import Sequence

import pulumi
import pulumi_gcp as gcp

from config import GCP_PROJECT, GCP_REGION

# Shared, environment-neutral resource names and import paths.
_ROUTER_NAME = "biocirv-router"
_NAT_NAME = "biocirv-nat"
_ROUTER_IMPORT_PATH = f"projects/{GCP_PROJECT}/regions/{GCP_REGION}/routers/{_ROUTER_NAME}"
_NAT_IMPORT_PATH = f"{_ROUTER_IMPORT_PATH}/{_NAT_NAME}"


@dataclass
class NetworkingResources:
    router: gcp.compute.Router
    nat: gcp.compute.RouterNat


def create_cloud_nat(
    depends_on: Sequence[pulumi.Resource] | None = None,
) -> NetworkingResources:
    """Import the shared Cloud Router + Cloud NAT on the default VPC.

    This enables Cloud Run services with Direct VPC egress
    (egress=ALL_TRAFFIC) to reach external endpoints (e.g. Google OAuth APIs)
    while still routing traffic through the VPC for internal ingress.

    The router and NAT are created once (manually or by the first stack) and
    then imported by every stack so Pulumi can reference them in the
    dependency graph.
    """
    router = gcp.compute.Router(
        "cloud-router",
        name=_ROUTER_NAME,
        region=GCP_REGION,
        network="default",
        opts=pulumi.ResourceOptions(
            depends_on=depends_on or [],
            import_=_ROUTER_IMPORT_PATH,
            retain_on_delete=True,
        ),
    )

    nat = gcp.compute.RouterNat(
        "cloud-nat",
        name=_NAT_NAME,
        router=router.name,
        region=GCP_REGION,
        nat_ip_allocate_option="AUTO_ONLY",
        source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
        opts=pulumi.ResourceOptions(
            depends_on=[router],
            import_=_NAT_IMPORT_PATH,
            retain_on_delete=True,
        ),
    )

    return NetworkingResources(router=router, nat=nat)
