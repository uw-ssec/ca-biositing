"""USDA data API endpoints.

This package contains USDA census and survey data endpoints.
"""

from __future__ import annotations
from fastapi import APIRouter

from .census import router as census_router

# Create USDA router with hierarchical prefix
router = APIRouter(prefix="/usda", tags=["USDA"])
router.include_router(census_router)
