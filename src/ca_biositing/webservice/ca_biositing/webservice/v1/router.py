"""API v1 main router.

This module aggregates all v1 endpoints into a single router.
"""

from __future__ import annotations

from fastapi import APIRouter

# Create the main v1 router
router = APIRouter(prefix="/v1")

# Include all endpoint routers
# Note: Most endpoints have been removed as they were outdated.
# Re-add them as they are rebuilt with the new data models.
