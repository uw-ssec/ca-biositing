"""Biomass CRUD endpoints.

This module provides REST API endpoints for biomass operations.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from ca_biositing.webservice.dependencies import PaginationDep, SessionDep
from ca_biositing.webservice.schemas.biomass import (
    BiomassCreate,
    BiomassResponse,
    BiomassUpdate,
)
from ca_biositing.webservice.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
)
from ca_biositing.webservice.services import biomass_service

router = APIRouter(prefix="/biomass", tags=["biomass"])


@router.get(
    "",
    response_model=PaginatedResponse[BiomassResponse],
    status_code=status.HTTP_200_OK,
    summary="List biomass entries",
    description="Get a paginated list of all biomass entries",
)
def list_biomass(
    session: SessionDep,
    pagination: PaginationDep,
) -> PaginatedResponse[BiomassResponse]:
    """Get a paginated list of biomass entries.
    
    Args:
        session: Database session
        pagination: Pagination parameters
        
    Returns:
        Paginated response with biomass entries
    """
    biomass_list, total = biomass_service.get_biomass_list(
        session, skip=pagination.skip, limit=pagination.limit
    )
    
    return PaginatedResponse(
        items=[BiomassResponse.model_validate(b) for b in biomass_list],
        pagination=PaginationInfo(
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            returned=len(biomass_list),
        ),
    )


@router.get(
    "/{biomass_id}",
    response_model=BiomassResponse,
    status_code=status.HTTP_200_OK,
    summary="Get biomass by ID",
    description="Get a specific biomass entry by its ID",
)
def get_biomass(biomass_id: int, session: SessionDep) -> BiomassResponse:
    """Get a specific biomass entry by ID.
    
    Args:
        biomass_id: ID of the biomass to retrieve
        session: Database session
        
    Returns:
        Biomass entry
        
    Raises:
        HTTPException: If biomass not found
    """
    biomass = biomass_service.get_biomass_by_id(session, biomass_id)
    if not biomass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Biomass with ID {biomass_id} not found",
        )
    return BiomassResponse.model_validate(biomass)


@router.post(
    "",
    response_model=BiomassResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create biomass",
    description="Create a new biomass entry",
)
def create_biomass(
    biomass_data: BiomassCreate,
    session: SessionDep,
) -> BiomassResponse:
    """Create a new biomass entry.
    
    Args:
        biomass_data: Biomass data to create
        session: Database session
        
    Returns:
        Created biomass entry
    """
    biomass = biomass_service.create_biomass(session, biomass_data)
    return BiomassResponse.model_validate(biomass)


@router.put(
    "/{biomass_id}",
    response_model=BiomassResponse,
    status_code=status.HTTP_200_OK,
    summary="Update biomass",
    description="Update an existing biomass entry",
)
def update_biomass(
    biomass_id: int,
    biomass_data: BiomassUpdate,
    session: SessionDep,
) -> BiomassResponse:
    """Update an existing biomass entry.
    
    Args:
        biomass_id: ID of the biomass to update
        biomass_data: Updated biomass data
        session: Database session
        
    Returns:
        Updated biomass entry
        
    Raises:
        HTTPException: If biomass not found
    """
    biomass = biomass_service.update_biomass(session, biomass_id, biomass_data)
    if not biomass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Biomass with ID {biomass_id} not found",
        )
    return BiomassResponse.model_validate(biomass)


@router.delete(
    "/{biomass_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete biomass",
    description="Delete a biomass entry",
)
def delete_biomass(biomass_id: int, session: SessionDep) -> MessageResponse:
    """Delete a biomass entry.
    
    Args:
        biomass_id: ID of the biomass to delete
        session: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If biomass not found
    """
    deleted = biomass_service.delete_biomass(session, biomass_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Biomass with ID {biomass_id} not found",
        )
    return MessageResponse(message=f"Biomass {biomass_id} deleted successfully")
