"""Pydantic schemas for biomass endpoints.

This module provides request and response schemas for biomass-related operations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# Base schemas
class BiomassBase(BaseModel):
    """Base schema for biomass data.

    Attributes:
        biomass_name: Name of the biomass
        primary_product_id: Reference to primary product
        taxonomy_id: Reference to taxonomy
        biomass_type_id: Reference to biomass type
        biomass_notes: Additional notes about the biomass
    """

    biomass_name: str = Field(..., description="Name of the biomass")
    primary_product_id: Optional[int] = Field(None, description="Primary product reference")
    taxonomy_id: Optional[int] = Field(None, description="Taxonomy reference")
    biomass_type_id: Optional[int] = Field(None, description="Biomass type reference")
    biomass_notes: Optional[str] = Field(None, description="Additional notes")


class BiomassCreate(BiomassBase):
    """Schema for creating a new biomass entry."""
    pass


class BiomassUpdate(BaseModel):
    """Schema for updating an existing biomass entry.

    All fields are optional to support partial updates.
    """

    biomass_name: Optional[str] = Field(None, description="Name of the biomass")
    primary_product_id: Optional[int] = Field(None, description="Primary product reference")
    taxonomy_id: Optional[int] = Field(None, description="Taxonomy reference")
    biomass_type_id: Optional[int] = Field(None, description="Biomass type reference")
    biomass_notes: Optional[str] = Field(None, description="Additional notes")


class BiomassResponse(BiomassBase):
    """Schema for biomass response data.

    Attributes:
        biomass_id: Unique identifier for the biomass
    """

    biomass_id: int = Field(..., description="Unique identifier")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
