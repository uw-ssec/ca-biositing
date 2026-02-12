from ..base import BaseEntity, LookupBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class SoilType(LookupBase, table=True):
    __tablename__ = "soil_type"



class LocationSoilType(BaseEntity, table=True):
    __tablename__ = "location_soil_type"

    location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    soil_type_id: Optional[int] = Field(default=None, foreign_key="soil_type.id")

    # Relationships
    location: Optional["LocationAddress"] = Relationship()
    soil_type: Optional["SoilType"] = Relationship()

