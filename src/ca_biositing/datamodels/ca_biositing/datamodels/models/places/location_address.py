from ..base import BaseEntity, LookupBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class LocationResolution(LookupBase, table=True):
    __tablename__ = "location_resolution"



class LocationAddress(BaseEntity, table=True):
    __tablename__ = "location_address"

    geography_id: Optional[str] = Field(default=None, foreign_key="place.geoid")
    address_line1: Optional[str] = Field(default=None)
    address_line2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)
    is_anonymous: Optional[bool] = Field(default=None)

    # Relationships
    geography: Optional["Place"] = Relationship()
