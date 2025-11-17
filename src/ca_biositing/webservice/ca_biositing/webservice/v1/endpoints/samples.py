"""Field sample CRUD endpoints.

This module provides REST API endpoints for field sample operations.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ca_biositing.datamodels.biomass import FieldSample
from ca_biositing.webservice.dependencies import PaginationDep, SessionDep
from ca_biositing.webservice.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
)
from ca_biositing.webservice.schemas.samples import (
    FieldSampleCreate,
    FieldSampleResponse,
    FieldSampleUpdate,
)

router = APIRouter(prefix="/samples", tags=["samples"])


@router.get(
    "",
    response_model=PaginatedResponse[FieldSampleResponse],
    status_code=status.HTTP_200_OK,
    summary="List field samples",
    description="Get a paginated list of all field samples",
)
def list_samples(
    session: SessionDep,
    pagination: PaginationDep,
) -> PaginatedResponse[FieldSampleResponse]:
    """Get a paginated list of field samples.

    Args:
        session: Database session
        pagination: Pagination parameters

    Returns:
        Paginated response with field samples
    """
    # Get total count
    count_statement = select(FieldSample)
    total = len(session.exec(count_statement).all())

    # Get paginated results
    statement = select(FieldSample).offset(pagination.skip).limit(pagination.limit)
    samples = session.exec(statement).all()

    return PaginatedResponse(
        items=[FieldSampleResponse.model_validate(s) for s in samples],
        pagination=PaginationInfo(
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            returned=len(samples),
        ),
    )


@router.get(
    "/{sample_id}",
    response_model=FieldSampleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get field sample by ID",
    description="Get a specific field sample by its ID",
)
def get_sample(sample_id: int, session: SessionDep) -> FieldSampleResponse:
    """Get a specific field sample by ID.

    Args:
        sample_id: ID of the sample to retrieve
        session: Database session

    Returns:
        Field sample entry

    Raises:
        HTTPException: If sample not found
    """
    sample = session.get(FieldSample, sample_id)
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found",
        )
    return FieldSampleResponse.model_validate(sample)


@router.post(
    "",
    response_model=FieldSampleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create field sample",
    description="Create a new field sample",
)
def create_sample(
    sample_data: FieldSampleCreate,
    session: SessionDep,
) -> FieldSampleResponse:
    """Create a new field sample.

    Args:
        sample_data: Sample data to create
        session: Database session

    Returns:
        Created field sample
    """
    sample = FieldSample(**sample_data.model_dump())
    session.add(sample)
    session.commit()
    session.refresh(sample)
    return FieldSampleResponse.model_validate(sample)


@router.put(
    "/{sample_id}",
    response_model=FieldSampleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update field sample",
    description="Update an existing field sample",
)
def update_sample(
    sample_id: int,
    sample_data: FieldSampleUpdate,
    session: SessionDep,
) -> FieldSampleResponse:
    """Update an existing field sample.

    Args:
        sample_id: ID of the sample to update
        sample_data: Updated sample data
        session: Database session

    Returns:
        Updated field sample

    Raises:
        HTTPException: If sample not found
    """
    sample = session.get(FieldSample, sample_id)
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found",
        )

    # Update only provided fields
    update_data = sample_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sample, key, value)

    session.add(sample)
    session.commit()
    session.refresh(sample)
    return FieldSampleResponse.model_validate(sample)


@router.delete(
    "/{sample_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete field sample",
    description="Delete a field sample",
)
def delete_sample(sample_id: int, session: SessionDep) -> MessageResponse:
    """Delete a field sample.

    Args:
        sample_id: ID of the sample to delete
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If sample not found
    """
    sample = session.get(FieldSample, sample_id)
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found",
        )

    session.delete(sample)
    session.commit()
    return MessageResponse(message=f"Sample {sample_id} deleted successfully")
