"""Dependencies for FastAPI endpoints.

This module provides dependency injection functions for database sessions,
authentication, and common query parameters.
"""

from __future__ import annotations

from typing import Annotated
from fastapi import Depends, Query
from sqlmodel import Session
from ca_biositing.datamodels.database import get_session


# Database session dependency
SessionDep = Annotated[Session, Depends(get_session)]


def pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
):
    """Common pagination parameters for list endpoints."""
    return {"skip": skip, "limit": limit}


# Pagination dependency
PaginationDep = Annotated[dict, Depends(pagination_params)]
