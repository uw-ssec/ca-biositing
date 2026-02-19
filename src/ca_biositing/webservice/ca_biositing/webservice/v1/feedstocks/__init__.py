"""Feedstocks API endpoints.

This package contains all feedstock-related endpoints including
USDA census/survey data, feedstock analysis, and resource availability.
"""

from __future__ import annotations
from fastapi import APIRouter

from .usda import router as usda_router
from .analysis import router as analysis_router
from .availability import router as availability_router

# Create feedstocks router and include all sub-routers
router = APIRouter(prefix="/feedstocks")
router.include_router(usda_router)
router.include_router(analysis_router)
router.include_router(availability_router)
