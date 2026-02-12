from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class ResourceAvailability(BaseEntity, table=True):
    __tablename__ = "resource_availability"

    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    from_month: Optional[int] = Field(default=None)
    to_month: Optional[int] = Field(default=None)
    year_round: Optional[bool] = Field(default=None)
    residue_factor_dry_tons_acre: Optional[float] = Field(default=None)
    residue_factor_wet_tons_acre: Optional[float] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    resource: Optional["Resource"] = Relationship()
    place: Optional["Place"] = Relationship()
