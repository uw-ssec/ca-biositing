"""Geographic location CRUD endpoints.

This module provides REST API endpoints for location operations.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ca_biositing.datamodels.geographic_locations import GeographicLocation
from ca_biositing.webservice.dependencies import PaginationDep, SessionDep
from ca_biositing.webservice.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
)
from ca_biositing.webservice.schemas.locations import (
    GeographicLocationCreate,
    GeographicLocationResponse,
    GeographicLocationUpdate,
)

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get(
    "",
    response_model=PaginatedResponse[GeographicLocationResponse],
    status_code=status.HTTP_200_OK,
    summary="List locations",
    description="Get a paginated list of all geographic locations",
)
def list_locations(
    session: SessionDep,
    pagination: PaginationDep,
) -> PaginatedResponse[GeographicLocationResponse]:
    """Get a paginated list of geographic locations.

    Args:
        session: Database session
        pagination: Pagination parameters

    Returns:
        Paginated response with locations
    """
    # Get total count
    count_statement = select(GeographicLocation)
    total = len(session.exec(count_statement).all())

    # Get paginated results
    statement = select(GeographicLocation).offset(pagination["skip"]).limit(pagination["limit"])
    locations = session.exec(statement).all()

    return PaginatedResponse(
        items=[GeographicLocationResponse.model_validate(l) for l in locations],
        pagination=PaginationInfo(
            total=total,
            skip=pagination["skip"],
            limit=pagination["limit"],
            returned=len(locations),
        ),
    )


@router.get(
    "/{location_id}",
    response_model=GeographicLocationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get location by ID",
    description="Get a specific geographic location by its ID",
)
def get_location(location_id: int, session: SessionDep) -> GeographicLocationResponse:
    """Get a specific geographic location by ID.

    Args:
        location_id: ID of the location to retrieve
        session: Database session

    Returns:
        Geographic location entry

    Raises:
        HTTPException: If location not found
    """
    location = session.get(GeographicLocation, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found",
        )
    return GeographicLocationResponse.model_validate(location)


@router.post(
    "",
    response_model=GeographicLocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create location",
    description="Create a new geographic location",
)
def create_location(
    location_data: GeographicLocationCreate,
    session: SessionDep,
) -> GeographicLocationResponse:
    """Create a new geographic location.

    Args:
        location_data: Location data to create
        session: Database session

    Returns:
        Created geographic location
    """
    location = GeographicLocation(**location_data.model_dump())
    session.add(location)
    session.commit()
    session.refresh(location)
    return GeographicLocationResponse.model_validate(location)


@router.put(
    "/{location_id}",
    response_model=GeographicLocationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update location",
    description="Update an existing geographic location",
)
def update_location(
    location_id: int,
    location_data: GeographicLocationUpdate,
    session: SessionDep,
) -> GeographicLocationResponse:
    """Update an existing geographic location.

    Args:
        location_id: ID of the location to update
        location_data: Updated location data
        session: Database session

    Returns:
        Updated geographic location

    Raises:
        HTTPException: If location not found
    """
    location = session.get(GeographicLocation, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found",
        )

    # Update only provided fields
    update_data = location_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(location, key, value)

    session.add(location)
    session.commit()
    session.refresh(location)
    return GeographicLocationResponse.model_validate(location)


@router.delete(
    "/{location_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete location",
    description="Delete a geographic location",
)
def delete_location(location_id: int, session: SessionDep) -> MessageResponse:
    """Delete a geographic location.

    Args:
        location_id: ID of the location to delete
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If location not found
    """
    location = session.get(GeographicLocation, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found",
        )

    session.delete(location)
    session.commit()
    return MessageResponse(message=f"Location {location_id} deleted successfully")
