"""API v1 main router.

This module aggregates all v1 endpoints into a single router.
"""

from __future__ import annotations

from fastapi import APIRouter

from ca_biositing.webservice.v1.feedstocks import router as feedstocks_router

# Create the main v1 router
router = APIRouter(prefix="/v1")

# Include all endpoint routers
router.include_router(feedstocks_router)
