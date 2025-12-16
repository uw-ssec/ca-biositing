"""API v1 main router.

This module aggregates all v1 endpoints into a single router.
"""

from __future__ import annotations

from fastapi import APIRouter

from ca_biositing.webservice.v1.endpoints import (
    biomass,
    experiments,
    health,
    locations,
    products,
    samples,
)

# Create the main v1 router
router = APIRouter(prefix="/v1")

# Include all endpoint routers
router.include_router(health.router)
router.include_router(biomass.router)
router.include_router(experiments.router)
router.include_router(samples.router)
router.include_router(locations.router)
router.include_router(products.router)
