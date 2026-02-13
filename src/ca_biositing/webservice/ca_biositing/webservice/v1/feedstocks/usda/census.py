"""USDA Census data API endpoints.

This module provides RESTful API endpoints for querying USDA census data.
Endpoints follow REST principles with resources in the URL path.
"""

from __future__ import annotations

from fastapi import APIRouter, Path

from ca_biositing.webservice.dependencies import SessionDep
from ca_biositing.webservice.services.usda_census_service import UsdaCensusService
from ca_biositing.webservice.v1.feedstocks.schemas import (
    CensusDataResponse,
    CensusListResponse,
)

router = APIRouter(prefix="/census", tags=["Census"])


@router.get(
    "/crops/{crop}/geoid/{geoid}/parameters/{parameter}",
    response_model=CensusDataResponse,
)
def get_census_data_by_crop(
    session: SessionDep,
    crop: str = Path(..., description="USDA crop name (e.g., CORN, SOYBEANS)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
    parameter: str = Path(..., description="Parameter name (e.g., acres, production)"),
) -> CensusDataResponse:
    """Get a single census parameter for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters/acres

    Args:
        session: Database session (injected)
        crop: USDA crop name
        geoid: Geographic identifier (county FIPS code)
        parameter: Parameter name to retrieve

    Returns:
        CensusDataResponse with the parameter value and metadata

    Raises:
        CropNotFoundException: If crop not found in database
        ParameterNotFoundException: If parameter not found for crop/geoid
    """
    data = UsdaCensusService.get_by_crop(session, crop, geoid, parameter)
    return CensusDataResponse(**data)


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters/{parameter}",
    response_model=CensusDataResponse,
)
def get_census_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., corn_grain, soybean_meal)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
    parameter: str = Path(..., description="Parameter name (e.g., acres, production)"),
) -> CensusDataResponse:
    """Get a single census parameter for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/census/resources/corn_grain/geoid/06001/parameters/acres

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)
        parameter: Parameter name to retrieve

    Returns:
        CensusDataResponse with the parameter value and metadata

    Raises:
        ResourceNotFoundException: If resource not found in database
        ParameterNotFoundException: If parameter not found for resource/geoid
    """
    data = UsdaCensusService.get_by_resource(session, resource, geoid, parameter)
    return CensusDataResponse(**data)


@router.get(
    "/crops/{crop}/geoid/{geoid}/parameters",
    response_model=CensusListResponse,
)
def list_census_data_by_crop(
    session: SessionDep,
    crop: str = Path(..., description="USDA crop name (e.g., CORN, SOYBEANS)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
) -> CensusListResponse:
    """List all available census parameters for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters

    Args:
        session: Database session (injected)
        crop: USDA crop name
        geoid: Geographic identifier (county FIPS code)

    Returns:
        CensusListResponse with list of all parameters and their values

    Raises:
        CropNotFoundException: If crop not found in database
        ParameterNotFoundException: If no data found for crop/geoid
    """
    data = UsdaCensusService.list_by_crop(session, crop, geoid)
    return CensusListResponse(**data)


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters",
    response_model=CensusListResponse,
)
def list_census_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., corn_grain, soybean_meal)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
) -> CensusListResponse:
    """List all available census parameters for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/census/resources/corn_grain/geoid/06001/parameters

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)

    Returns:
        CensusListResponse with list of all parameters and their values

    Raises:
        ResourceNotFoundException: If resource not found in database
        ParameterNotFoundException: If no data found for resource/geoid
    """
    data = UsdaCensusService.list_by_resource(session, resource, geoid)
    return CensusListResponse(**data)
