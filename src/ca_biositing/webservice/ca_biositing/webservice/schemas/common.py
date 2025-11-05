"""Common schemas used across multiple endpoints.

This module provides base schemas for pagination, responses, and other
shared data structures.
"""

from __future__ import annotations

from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Attributes:
        status: Status of the service (healthy/unhealthy)
        version: API version
        database: Database connection status
    """

    status: str = Field(..., description="Overall service status")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database connection status")


class PaginationInfo(BaseModel):
    """Pagination metadata.
    
    Attributes:
        total: Total number of items available
        skip: Number of items skipped
        limit: Maximum number of items returned
        returned: Actual number of items returned
    """

    total: int = Field(..., description="Total number of items available")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Maximum number of items per page")
    returned: int = Field(..., description="Actual number of items returned")


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.
    
    Attributes:
        items: List of items
        pagination: Pagination metadata
    """

    items: List[T] = Field(..., description="List of items")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class ErrorResponse(BaseModel):
    """Standard error response.
    
    Attributes:
        detail: Error message
        error_code: Optional error code for programmatic handling
    """

    detail: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Error code")


class MessageResponse(BaseModel):
    """Simple message response.
    
    Attributes:
        message: The message text
    """

    message: str = Field(..., description="Response message")
