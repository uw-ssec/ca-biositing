"""USDA Survey data API endpoints.

This module provides RESTful API endpoints for querying USDA survey data.
Endpoints follow REST principles with resources in the URL path.
"""

from __future__ import annotations

from fastapi import APIRouter, Path

from ca_biositing.webservice.dependencies import SessionDep
from ca_biositing.webservice.services.usda_survey_service import UsdaSurveyService
from ca_biositing.webservice.v1.feedstocks.schemas import (
    DiscoveryResponse,
    SurveyDataResponse,
    SurveyListResponse,
)

router = APIRouter(prefix="/survey", tags=["Survey"])


@router.get("/crops", response_model=DiscoveryResponse)
def list_survey_crops(session: SessionDep) -> DiscoveryResponse:
    """List all distinct USDA crop names available for survey queries.

    Example:
        GET /v1/feedstocks/usda/survey/crops

    Returns:
        DiscoveryResponse with list of crop name strings
    """
    return DiscoveryResponse(values=UsdaSurveyService.list_crops(session))


@router.get("/resources", response_model=DiscoveryResponse)
def list_survey_resources(session: SessionDep) -> DiscoveryResponse:
    """List all distinct resource names available for survey queries.

    Example:
        GET /v1/feedstocks/usda/survey/resources

    Returns:
        DiscoveryResponse with list of resource name strings
    """
    return DiscoveryResponse(values=UsdaSurveyService.list_resources(session))


@router.get("/geoids", response_model=DiscoveryResponse)
def list_survey_geoids(session: SessionDep) -> DiscoveryResponse:
    """List all distinct geoids available for survey queries.

    Example:
        GET /v1/feedstocks/usda/survey/geoids

    Returns:
        DiscoveryResponse with list of geoid strings
    """
    return DiscoveryResponse(values=UsdaSurveyService.list_geoids(session))


@router.get("/parameters", response_model=DiscoveryResponse)
def list_survey_parameters(session: SessionDep) -> DiscoveryResponse:
    """List all distinct parameter names available for survey queries.

    Example:
        GET /v1/feedstocks/usda/survey/parameters

    Returns:
        DiscoveryResponse with list of parameter name strings
    """
    return DiscoveryResponse(values=UsdaSurveyService.list_parameters(session))


@router.get(
    "/crops/{crop}/geoid/{geoid}/parameters/{parameter}",
    response_model=SurveyDataResponse,
)
def get_survey_data_by_crop(
    session: SessionDep,
    crop: str = Path(
        ...,
        description=(
            "USDA crop name (e.g., corn, wheat, tomatoes). "
            "Case-insensitive. "
            "Use GET /v1/feedstocks/usda/survey/crops to discover available values."
        ),
    ),
    geoid: str = Path(
        ...,
        description=(
            "Geographic identifier (e.g., 06047, 06077, 06099). "
            "Use GET /v1/feedstocks/usda/survey/geoids to discover available values."
        ),
    ),
    parameter: str = Path(
        ...,
        description=(
            "Parameter name (e.g., area harvested, production). "
            "Use GET /v1/feedstocks/usda/survey/parameters to discover available values."
        ),
    ),
) -> SurveyDataResponse:
    """Get a single survey parameter for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/survey/crops/wheat/geoid/06047/parameters/area harvested

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
    resource: str = Path(
        ...,
        description=(
            "Resource name mapped to a USDA crop (e.g., corn stover whole, wheat straw). "
            "Case-insensitive. "
            "Use GET /v1/feedstocks/usda/survey/resources to discover available values."
        ),
    ),
    geoid: str = Path(
        ...,
        description=(
            "Geographic identifier (e.g., 06047, 06077, 06099). "
            "Use GET /v1/feedstocks/usda/survey/geoids to discover available values."
        ),
    ),
    parameter: str = Path(
        ...,
        description=(
            "Parameter name (e.g., area harvested, production). "
            "Use GET /v1/feedstocks/usda/survey/parameters to discover available values."
        ),
    ),
) -> SurveyDataResponse:
    """Get a single survey parameter for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/survey/resources/wheat straw/geoid/06047/parameters/area harvested

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
    crop: str = Path(
        ...,
        description=(
            "USDA crop name (e.g., corn, wheat, tomatoes). "
            "Case-insensitive. "
            "Use GET /v1/feedstocks/usda/survey/crops to discover available values."
        ),
    ),
    geoid: str = Path(
        ...,
        description=(
            "Geographic identifier (e.g., 06047, 06077, 06099). "
            "Use GET /v1/feedstocks/usda/survey/geoids to discover available values."
        ),
    ),
) -> SurveyListResponse:
    """List all available survey parameters for a specific crop and geographic area.

    Example:
        GET /v1/feedstocks/usda/survey/crops/wheat/geoid/06047/parameters

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
    resource: str = Path(
        ...,
        description=(
            "Resource name mapped to a USDA crop (e.g., corn stover whole, wheat straw). "
            "Case-insensitive. "
            "Use GET /v1/feedstocks/usda/survey/resources to discover available values."
        ),
    ),
    geoid: str = Path(
        ...,
        description=(
            "Geographic identifier (e.g., 06047, 06077, 06099). "
            "Use GET /v1/feedstocks/usda/survey/geoids to discover available values."
        ),
    ),
) -> SurveyListResponse:
    """List all available survey parameters for a specific resource and geographic area.

    Resources are mapped to USDA crops internally via the resource mapping table.

    Example:
        GET /v1/feedstocks/usda/survey/resources/wheat straw/geoid/06047/parameters

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
