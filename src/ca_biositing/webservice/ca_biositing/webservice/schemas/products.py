"""Pydantic schemas for product endpoints.

This module provides request and response schemas for primary product operations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PrimaryProductBase(BaseModel):
    """Base schema for primary product data.
    
    Attributes:
        primary_product_name: Name of the primary product
    """

    primary_product_name: str = Field(..., description="Name of the primary product")


class PrimaryProductCreate(PrimaryProductBase):
    """Schema for creating a new primary product."""
    pass


class PrimaryProductUpdate(BaseModel):
    """Schema for updating an existing primary product.
    
    All fields are optional to support partial updates.
    """

    primary_product_name: Optional[str] = Field(None, description="Name of the primary product")


class PrimaryProductResponse(PrimaryProductBase):
    """Schema for primary product response data.
    
    Attributes:
        primary_product_id: Unique identifier for the product
    """

    primary_product_id: int = Field(..., description="Unique identifier")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
