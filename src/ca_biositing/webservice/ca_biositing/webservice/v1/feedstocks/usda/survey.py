"""USDA Survey data API endpoints.

This module provides RESTful API endpoints for querying USDA survey data.
Endpoints follow REST principles with resources in the URL path.
"""

from __future__ import annotations

from fastapi import APIRouter, Path

from ca_biositing.webservice.dependencies import SessionDep
from ca_biositing.webservice.services.usda_survey_service import UsdaSurveyService
from ca_biositing.webservice.v1.feedstocks.schemas import (
    SurveyDataResponse,
    SurveyListResponse,
)

router = APIRouter(prefix="/survey", tags=["Survey"])


@router.get(
    "/crops/{crop}/geoid/{geoid}/parameters/{parameter}",
    response_model=SurveyDataResponse,
)
def get_survey_data_by_crop(
    session: SessionDep,
    crop: str = Path(..., description="USDA crop name (e.g., CORN, SOYBEANS)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
    parameter: str = Path(..., description="Parameter name (e.g., acres, production)"),
) -> SurveyDataResponse:
    """Get a single survey parameter for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/survey/crops/CORN/geoid/06001/parameters/acres

    Args:
        session: Database session (injected)
        crop: USDA crop name
        geoid: Geographic identifier (county FIPS code)
        parameter: Parameter name to retrieve

    Returns:
        SurveyDataResponse with the parameter value and survey metadata

    Raises:
        CropNotFoundException: If crop not found in database
        ParameterNotFoundException: If parameter not found for crop/geoid
    """
    data = UsdaSurveyService.get_by_crop(session, crop, geoid, parameter)
    return SurveyDataResponse(**data)


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters/{parameter}",
    response_model=SurveyDataResponse,
)
def get_survey_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., corn_grain, soybean_meal)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
    parameter: str = Path(..., description="Parameter name (e.g., acres, production)"),
) -> SurveyDataResponse:
    """Get a single survey parameter for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/survey/resources/corn_grain/geoid/06001/parameters/acres

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)
        parameter: Parameter name to retrieve

    Returns:
        SurveyDataResponse with the parameter value and survey metadata

    Raises:
        ResourceNotFoundException: If resource not found in database
        ParameterNotFoundException: If parameter not found for resource/geoid
    """
    data = UsdaSurveyService.get_by_resource(session, resource, geoid, parameter)
    return SurveyDataResponse(**data)


@router.get(
    "/crops/{crop}/geoid/{geoid}/parameters",
    response_model=SurveyListResponse,
)
def list_survey_data_by_crop(
    session: SessionDep,
    crop: str = Path(..., description="USDA crop name (e.g., CORN, SOYBEANS)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
) -> SurveyListResponse:
    """List all available survey parameters for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/survey/crops/CORN/geoid/06001/parameters

    Args:
        session: Database session (injected)
        crop: USDA crop name
        geoid: Geographic identifier (county FIPS code)

    Returns:
        SurveyListResponse with list of all parameters and their values

    Raises:
        CropNotFoundException: If crop not found in database
        ParameterNotFoundException: If no data found for crop/geoid
    """
    data = UsdaSurveyService.list_by_crop(session, crop, geoid)
    return SurveyListResponse(**data)


@router.get(
    "/resources/{resource}/geoid/{geoid}/parameters",
    response_model=SurveyListResponse,
)
def list_survey_data_by_resource(
    session: SessionDep,
    resource: str = Path(..., description="Resource name (e.g., corn_grain, soybean_meal)"),
    geoid: str = Path(..., description="Geographic identifier (e.g., 06001)"),
) -> SurveyListResponse:
    """List all available survey parameters for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/survey/resources/corn_grain/geoid/06001/parameters

    Args:
        session: Database session (injected)
        resource: Resource name
        geoid: Geographic identifier (county FIPS code)

    Returns:
        SurveyListResponse with list of all parameters and their values

    Raises:
        ResourceNotFoundException: If resource not found in database
        ParameterNotFoundException: If no data found for resource/geoid
    """
    data = UsdaSurveyService.list_by_resource(session, resource, geoid)
    return SurveyListResponse(**data)
