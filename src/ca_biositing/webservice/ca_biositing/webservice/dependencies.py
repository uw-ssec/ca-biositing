"""Dependencies for FastAPI endpoints.

This module provides dependency injection functions for database sessions,
authentication, and common query parameters.
"""

from __future__ import annotations

from typing import Annotated, Generator

from fastapi import Depends, Query
from sqlmodel import Session

from ca_biositing.datamodels.database import get_session


# Database session dependency
SessionDep = Annotated[Session, Depends(get_session)]


class PaginationParams:
    """Common pagination parameters for list endpoints.
    
    Attributes:
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
    """

    def __init__(
        self,
        skip: Annotated[int, Query(ge=0, description="Number of records to skip")] = 0,
        limit: Annotated[
            int, Query(ge=1, le=100, description="Maximum number of records to return")
        ] = 50,
    ):
        self.skip = skip
        self.limit = limit


# Pagination dependency
PaginationDep = Annotated[PaginationParams, Depends()]
