"""Pydantic schemas for experiments endpoints.

This module provides request and response schemas for experiment-related operations.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ExperimentBase(BaseModel):
    """Base schema for experiment data.
    
    Attributes:
        exper_uuid: Unique UUID for the experiment
        gsheet_exper_id: Google Sheet experiment ID
        analysis_type_id: Reference to analysis type
        analysis_abbrev_id: Reference to analysis abbreviation
        exper_start_date: Experiment start date
        exper_duration: Duration of the experiment
        exper_duration_unit_id: Reference to duration unit
        exper_location_id: Reference to experiment location
        exper_description: Description of the experiment
    """

    exper_uuid: Optional[str] = Field(None, description="Unique UUID for the experiment")
    gsheet_exper_id: Optional[int] = Field(None, description="Google Sheet experiment ID")
    analysis_type_id: Optional[int] = Field(None, description="Analysis type reference")
    analysis_abbrev_id: Optional[int] = Field(None, description="Analysis abbreviation reference")
    exper_start_date: Optional[date] = Field(None, description="Experiment start date")
    exper_duration: Optional[Decimal] = Field(None, description="Experiment duration")
    exper_duration_unit_id: Optional[int] = Field(None, description="Duration unit reference")
    exper_location_id: Optional[int] = Field(None, description="Experiment location reference")
    exper_description: Optional[str] = Field(None, description="Experiment description")


class ExperimentCreate(ExperimentBase):
    """Schema for creating a new experiment."""
    pass


class ExperimentUpdate(BaseModel):
    """Schema for updating an existing experiment.
    
    All fields are optional to support partial updates.
    """

    exper_uuid: Optional[str] = Field(None, description="Unique UUID for the experiment")
    gsheet_exper_id: Optional[int] = Field(None, description="Google Sheet experiment ID")
    analysis_type_id: Optional[int] = Field(None, description="Analysis type reference")
    analysis_abbrev_id: Optional[int] = Field(None, description="Analysis abbreviation reference")
    exper_start_date: Optional[date] = Field(None, description="Experiment start date")
    exper_duration: Optional[Decimal] = Field(None, description="Experiment duration")
    exper_duration_unit_id: Optional[int] = Field(None, description="Duration unit reference")
    exper_location_id: Optional[int] = Field(None, description="Experiment location reference")
    exper_description: Optional[str] = Field(None, description="Experiment description")


class ExperimentResponse(ExperimentBase):
    """Schema for experiment response data.
    
    Attributes:
        experiment_id: Unique identifier for the experiment
    """

    experiment_id: int = Field(..., description="Unique identifier")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
