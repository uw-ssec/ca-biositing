"""Pydantic schemas for sample endpoints.

This module provides request and response schemas for field sample operations.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class FieldSampleBase(BaseModel):
    """Base schema for field sample data.
    
    Attributes:
        biomass_id: Reference to biomass
        sample_name: Name of the sample
        source_codename_id: Anonymized source identifier
        data_source_id: Reference to data source
        location_id: Reference to geographic location
        field_storage_id: Reference to field storage
        field_storage_duration_value: Duration value for field storage
        field_storage_duration_unit_id: Reference to unit of storage duration
        collection_timestamp: Sample collection timestamp
        collection_method_id: Reference to collection method
        harvest_method_id: Reference to harvest method
        harvest_date: Harvest date
        amount_collected_kg: Amount collected in kilograms
        provider_id: Reference to provider
        collector_id: Reference to collector
        basic_sample_info_note: Additional notes
    """

    biomass_id: int = Field(..., description="Reference to biomass")
    sample_name: str = Field(..., description="Name of the sample")
    source_codename_id: Optional[int] = Field(None, description="Anonymized source identifier")
    data_source_id: Optional[int] = Field(None, description="Data source reference")
    location_id: Optional[int] = Field(None, description="Geographic location reference")
    field_storage_id: Optional[int] = Field(None, description="Field storage reference")
    field_storage_duration_value: Optional[Decimal] = Field(None, description="Storage duration value")
    field_storage_duration_unit_id: Optional[int] = Field(None, description="Storage duration unit reference")
    collection_timestamp: Optional[datetime] = Field(None, description="Collection timestamp")
    collection_method_id: Optional[int] = Field(None, description="Collection method reference")
    harvest_method_id: Optional[int] = Field(None, description="Harvest method reference")
    harvest_date: Optional[date] = Field(None, description="Harvest date")
    amount_collected_kg: Optional[Decimal] = Field(None, description="Amount collected (kg)")
    provider_id: Optional[int] = Field(None, description="Provider reference")
    collector_id: Optional[int] = Field(None, description="Collector reference")
    basic_sample_info_note: Optional[str] = Field(None, description="Additional notes")


class FieldSampleCreate(FieldSampleBase):
    """Schema for creating a new field sample."""
    pass


class FieldSampleUpdate(BaseModel):
    """Schema for updating an existing field sample.
    
    All fields are optional to support partial updates.
    """

    biomass_id: Optional[int] = Field(None, description="Reference to biomass")
    sample_name: Optional[str] = Field(None, description="Name of the sample")
    source_codename_id: Optional[int] = Field(None, description="Anonymized source identifier")
    data_source_id: Optional[int] = Field(None, description="Data source reference")
    location_id: Optional[int] = Field(None, description="Geographic location reference")
    field_storage_id: Optional[int] = Field(None, description="Field storage reference")
    field_storage_duration_value: Optional[Decimal] = Field(None, description="Storage duration value")
    field_storage_duration_unit_id: Optional[int] = Field(None, description="Storage duration unit reference")
    collection_timestamp: Optional[datetime] = Field(None, description="Collection timestamp")
    collection_method_id: Optional[int] = Field(None, description="Collection method reference")
    harvest_method_id: Optional[int] = Field(None, description="Harvest method reference")
    harvest_date: Optional[date] = Field(None, description="Harvest date")
    amount_collected_kg: Optional[Decimal] = Field(None, description="Amount collected (kg)")
    provider_id: Optional[int] = Field(None, description="Provider reference")
    collector_id: Optional[int] = Field(None, description="Collector reference")
    basic_sample_info_note: Optional[str] = Field(None, description="Additional notes")


class FieldSampleResponse(FieldSampleBase):
    """Schema for field sample response data.
    
    Attributes:
        sample_id: Unique identifier for the sample
        created_at: Timestamp when the record was created
    """

    sample_id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
