from ..base import BaseEntity
from datetime import date
from decimal import Decimal
from sqlmodel import Field, Relationship
from typing import Optional


class ResourceCounterfactual(BaseEntity, table=True):
    __tablename__ = "resource_counterfactual"

    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    counterfactual_description: Optional[str] = Field(default=None)
    animal_bedding_percent: Optional[Decimal] = Field(default=None)
    animal_bedding_source_id: Optional[int] = Field(default=None)
    animal_feed_percent: Optional[Decimal] = Field(default=None)
    animal_feed_source_id: Optional[int] = Field(default=None)
    bioelectricty_percent: Optional[Decimal] = Field(default=None)
    bioelectricty_source_id: Optional[int] = Field(default=None)
    burn_percent: Optional[Decimal] = Field(default=None)
    burn_source_id: Optional[int] = Field(default=None)
    compost_percent: Optional[Decimal] = Field(default=None)
    compost_source_id: Optional[int] = Field(default=None)
    landfill_percent: Optional[Decimal] = Field(default=None)
    landfill_source_id: Optional[int] = Field(default=None)
    counterfactual_date: Optional[date] = Field(default=None)

    # Relationships
    place: Optional["Place"] = Relationship()
    resource: Optional["Resource"] = Relationship()
