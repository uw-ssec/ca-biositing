"""Health check and status endpoints.

This module provides endpoints for checking the health and status of the API
and its dependencies.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from sqlmodel import select

from ca_biositing.webservice.dependencies import SessionDep
from ca_biositing.webservice.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health status of the API and its dependencies",
)
def health_check(session: SessionDep) -> HealthResponse:
    """Check the health of the API and database connection.
    
    Args:
        session: Database session dependency
        
    Returns:
        HealthResponse with status information
    """
    # Check database connectivity
    try:
        # Simple query to test database connection
        session.exec(select(1)).first()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Determine overall status
    overall_status = "healthy" if db_status == "connected" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        version="0.1.0",
        database=db_status,
    )
