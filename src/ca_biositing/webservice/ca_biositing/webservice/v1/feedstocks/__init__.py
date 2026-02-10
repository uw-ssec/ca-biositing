"""Feedstocks API endpoints.

This package contains all feedstock-related endpoints including
USDA census/survey data and feedstock analysis.
"""

from __future__ import annotations

from fastapi import APIRouter

from .usda import router as usda_router

# Create feedstocks router and include USDA endpoints
router = APIRouter(prefix="/feedstocks")
router.include_router(usda_router)
