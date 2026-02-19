"""Common Pydantic schemas for feedstock API responses.

This module defines reusable response models for consistent API responses
across all feedstock endpoints.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class DataItemResponse(BaseModel):
    """Individual data item in list responses.

    Used when listing all parameters for a crop/resource/geoid combination.
    Each item represents one parameter with its value and metadata.
    """

    parameter: str = Field(..., description="Parameter name")
    value: Optional[float] = Field(None, description="Parameter value (may be null if not available)")
    unit: str = Field(..., description="Unit of measurement")
    dimension: Optional[str] = Field(None, description="Dimension name (if applicable)")
    dimension_value: Optional[float] = Field(
        None, description="Dimension value (if applicable)"
    )
    dimension_unit: Optional[str] = Field(
        None, description="Dimension unit (if applicable)"
    )


class CensusDataResponse(BaseModel):
    """Response for single USDA census parameter.

    Returned when requesting a specific parameter for a crop/resource and geoid.
    """

    usda_crop: Optional[str] = Field(None, description="USDA crop name (if queried by crop)")
    resource: Optional[str] = Field(None, description="Resource name (if queried by resource)")
    geoid: str = Field(..., description="Geographic identifier")
    parameter: str = Field(..., description="Parameter name")
    value: Optional[float] = Field(None, description="Parameter value (may be null if not available)")
    unit: str = Field(..., description="Unit of measurement")
    dimension: Optional[str] = Field(None, description="Dimension name (if applicable)")
    dimension_value: Optional[float] = Field(
        None, description="Dimension value (if applicable)"
    )
    dimension_unit: Optional[str] = Field(
        None, description="Dimension unit (if applicable)"
    )


class CensusListResponse(BaseModel):
    """Response for list of USDA census parameters.

    Returned when listing all parameters for a crop/resource and geoid.
    """

    usda_crop: Optional[str] = Field(None, description="USDA crop name (if queried by crop)")
    resource: Optional[str] = Field(None, description="Resource name (if queried by resource)")
    geoid: str = Field(..., description="Geographic identifier")
    data: list[DataItemResponse] = Field(..., description="List of parameter data")


class SurveyDataResponse(BaseModel):
    """Response for single USDA survey parameter.

    Similar to CensusDataResponse but for survey data, which includes
    additional survey-specific metadata fields.
    """

    usda_crop: Optional[str] = Field(None, description="USDA crop name (if queried by crop)")
    resource: Optional[str] = Field(None, description="Resource name (if queried by resource)")
    geoid: str = Field(..., description="Geographic identifier")
    parameter: str = Field(..., description="Parameter name")
    value: Optional[float] = Field(None, description="Parameter value (may be null if not available)")
    unit: str = Field(..., description="Unit of measurement")
    dimension: Optional[str] = Field(None, description="Dimension name (if applicable)")
    dimension_value: Optional[float] = Field(
        None, description="Dimension value (if applicable)"
    )
    dimension_unit: Optional[str] = Field(
        None, description="Dimension unit (if applicable)"
    )
    survey_program: Optional[str] = Field(None, description="Survey program name")
    survey_period: Optional[str] = Field(None, description="Survey period")
    reference_month: Optional[int] = Field(None, description="Reference month (1-12)")
    seasonal_flag: Optional[bool] = Field(None, description="Whether data is seasonal")


class SurveyListResponse(BaseModel):
    """Response for list of USDA survey parameters.

    Returned when listing all parameters for a crop/resource and geoid.
    """

    usda_crop: Optional[str] = Field(None, description="USDA crop name (if queried by crop)")
    resource: Optional[str] = Field(None, description="Resource name (if queried by resource)")
    geoid: str = Field(..., description="Geographic identifier")
    data: list[DataItemResponse] = Field(..., description="List of parameter data")


class AnalysisDataResponse(BaseModel):
    """Response for single feedstock analysis parameter.

    Returned when requesting a specific analysis parameter for a resource and geoid.
    """

    resource: str = Field(..., description="Resource name")
    geoid: str = Field(..., description="Geographic identifier")
    parameter: str = Field(..., description="Parameter name")
    value: Optional[float] = Field(None, description="Parameter value (may be null if not available)")
    unit: str = Field(..., description="Unit of measurement")


class AnalysisListResponse(BaseModel):
    """Response for list of feedstock analysis parameters.

    Returned when listing all analysis parameters for a resource and geoid.
    """

    resource: str = Field(..., description="Resource name")
    geoid: str = Field(..., description="Geographic identifier")
    data: list[DataItemResponse] = Field(..., description="List of parameter data")


class AvailabilityResponse(BaseModel):
    """Response for resource availability data.

    Returned when requesting seasonal availability for a resource and geoid.
    """

    resource: str = Field(..., description="Resource name")
    geoid: str = Field(..., description="Geographic identifier")
    from_month: int = Field(..., ge=1, le=12, description="Starting month (1-12)")
    to_month: int = Field(..., ge=1, le=12, description="Ending month (1-12)")
