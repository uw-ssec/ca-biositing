"""Feedstock Analysis data API endpoints.

This module provides RESTful API endpoints for querying feedstock analysis data
(proximate, ultimate, compositional analysis).
Endpoints follow REST principles with resources in the URL path.
"""

from __future__ import annotations

from fastapi import APIRouter, Path

from ca_biositing.webservice.dependencies import SessionDep
from ca_biositing.webservice.services.analysis_service import AnalysisService
from ca_biositing.webservice.v1.feedstocks.schemas import (
    AnalysisDataResponse,
    AnalysisListResponse,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters/{parameter}",
    response_model=AnalysisDataResponse,
)
def get_analysis_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., almond_hulls, corn_stover)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
    parameter: str = Path(..., description="Parameter name (e.g., ash, moisture)"),
) -> AnalysisDataResponse:
    """Get a single analysis parameter for a specific resource and geographic area.

    Queries analysis data from proximate, ultimate, and compositional analysis records.

    Example:
        GET /v1/feedstocks/analysis/resources/almond_hulls/geoid/06001/parameters/ash

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)
        parameter: Parameter name to retrieve

    Returns:
        AnalysisDataResponse with the parameter value and metadata

    Raises:
        ResourceNotFoundException: If resource not found in database
        ParameterNotFoundException: If parameter not found for resource/geoid
    """
    data = AnalysisService.get_by_resource(session, resource, geoid, parameter)
    return AnalysisDataResponse(**data)


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters",
    response_model=AnalysisListResponse,
)
def list_analysis_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., almond_hulls, corn_stover)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
) -> AnalysisListResponse:
    """List all analysis parameters for a specific resource and geographic area.

    Queries all available analysis data from proximate, ultimate, and compositional records.

    Example:
        GET /v1/feedstocks/analysis/resources/almond_hulls/geoid/06001/parameters

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)

    Returns:
        AnalysisListResponse with all available parameters and their values

    Raises:
        ResourceNotFoundException: If resource not found in database
    """
    data = AnalysisService.list_by_resource(session, resource, geoid)
    return AnalysisListResponse(**data)
