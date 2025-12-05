"""Experiment CRUD endpoints.

This module provides REST API endpoints for experiment operations.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from ca_biositing.webservice.dependencies import PaginationDep, SessionDep
from ca_biositing.webservice.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
)
from ca_biositing.webservice.schemas.experiments import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentUpdate,
)
from ca_biositing.webservice.services import experiment_service

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get(
    "",
    response_model=PaginatedResponse[ExperimentResponse],
    status_code=status.HTTP_200_OK,
    summary="List experiments",
    description="Get a paginated list of all experiments",
)
def list_experiments(
    session: SessionDep,
    pagination: PaginationDep,
) -> PaginatedResponse[ExperimentResponse]:
    """Get a paginated list of experiments.

    Args:
        session: Database session
        pagination: Pagination parameters

    Returns:
        Paginated response with experiments
    """
    experiments, total = experiment_service.get_experiment_list(
        session, skip=pagination["skip"], limit=pagination["limit"]
    )

    return PaginatedResponse(
        items=[ExperimentResponse.model_validate(e) for e in experiments],
        pagination=PaginationInfo(
            total=total,
            skip=pagination["skip"],
            limit=pagination["limit"],
            returned=len(experiments),
        ),
    )


@router.get(
    "/{experiment_id}",
    response_model=ExperimentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get experiment by ID",
    description="Get a specific experiment by its ID",
)
def get_experiment(experiment_id: int, session: SessionDep) -> ExperimentResponse:
    """Get a specific experiment by ID.

    Args:
        experiment_id: ID of the experiment to retrieve
        session: Database session

    Returns:
        Experiment entry

    Raises:
        HTTPException: If experiment not found
    """
    experiment = experiment_service.get_experiment_by_id(session, experiment_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with ID {experiment_id} not found",
        )
    return ExperimentResponse.model_validate(experiment)


@router.post(
    "",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create experiment",
    description="Create a new experiment",
)
def create_experiment(
    experiment_data: ExperimentCreate,
    session: SessionDep,
) -> ExperimentResponse:
    """Create a new experiment.

    Args:
        experiment_data: Experiment data to create
        session: Database session

    Returns:
        Created experiment
    """
    experiment = experiment_service.create_experiment(session, experiment_data)
    return ExperimentResponse.model_validate(experiment)


@router.put(
    "/{experiment_id}",
    response_model=ExperimentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update experiment",
    description="Update an existing experiment",
)
def update_experiment(
    experiment_id: int,
    experiment_data: ExperimentUpdate,
    session: SessionDep,
) -> ExperimentResponse:
    """Update an existing experiment.

    Args:
        experiment_id: ID of the experiment to update
        experiment_data: Updated experiment data
        session: Database session

    Returns:
        Updated experiment

    Raises:
        HTTPException: If experiment not found
    """
    experiment = experiment_service.update_experiment(
        session, experiment_id, experiment_data
    )
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with ID {experiment_id} not found",
        )
    return ExperimentResponse.model_validate(experiment)


@router.delete(
    "/{experiment_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete experiment",
    description="Delete an experiment",
)
def delete_experiment(experiment_id: int, session: SessionDep) -> MessageResponse:
    """Delete an experiment.

    Args:
        experiment_id: ID of the experiment to delete
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If experiment not found
    """
    deleted = experiment_service.delete_experiment(session, experiment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiment with ID {experiment_id} not found",
        )
    return MessageResponse(message=f"Experiment {experiment_id} deleted successfully")
