"""Pydantic schemas for geographic location endpoints.

This module provides request and response schemas for location-related operations.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class GeographicLocationBase(BaseModel):
    """Base schema for geographic location data.

    Attributes:
        street_address_id: Reference to street address
        city_id: Reference to city
        zip_id: Reference to ZIP code
        county_id: Reference to county
        state_id: Reference to state
        region_id: Reference to region
        fips_id: Reference to FIPS code
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_resolution_id: Reference to location resolution
        is_anonymous: Whether the location is anonymized
    """

    street_address_id: Optional[int] = Field(None, description="Street address reference")
    city_id: Optional[int] = Field(None, description="City reference")
    zip_id: Optional[int] = Field(None, description="ZIP code reference")
    county_id: Optional[int] = Field(None, description="County reference")
    state_id: Optional[int] = Field(None, description="State reference")
    region_id: Optional[int] = Field(None, description="Region reference")
    fips_id: Optional[int] = Field(None, description="FIPS code reference")
    latitude: Optional[Decimal] = Field(None, description="Latitude coordinate")
    longitude: Optional[Decimal] = Field(None, description="Longitude coordinate")
    location_resolution_id: Optional[int] = Field(None, description="Location resolution reference")
    is_anonymous: Optional[bool] = Field(None, description="Whether location is anonymized")


class GeographicLocationCreate(GeographicLocationBase):
    """Schema for creating a new geographic location."""
    pass


class GeographicLocationUpdate(BaseModel):
    """Schema for updating an existing geographic location.

    All fields are optional to support partial updates.
    """

    street_address_id: Optional[int] = Field(None, description="Street address reference")
    city_id: Optional[int] = Field(None, description="City reference")
    zip_id: Optional[int] = Field(None, description="ZIP code reference")
    county_id: Optional[int] = Field(None, description="County reference")
    state_id: Optional[int] = Field(None, description="State reference")
    region_id: Optional[int] = Field(None, description="Region reference")
    fips_id: Optional[int] = Field(None, description="FIPS code reference")
    latitude: Optional[Decimal] = Field(None, description="Latitude coordinate")
    longitude: Optional[Decimal] = Field(None, description="Longitude coordinate")
    location_resolution_id: Optional[int] = Field(None, description="Location resolution reference")
    is_anonymous: Optional[bool] = Field(None, description="Whether location is anonymized")


class GeographicLocationResponse(GeographicLocationBase):
    """Schema for geographic location response data.

    Attributes:
        location_id: Unique identifier for the location
    """

    location_id: int = Field(..., description="Unique identifier")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
