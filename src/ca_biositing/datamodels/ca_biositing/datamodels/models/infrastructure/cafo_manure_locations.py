from datetime import date
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class InfrastructureCafoManureLocations(SQLModel, table=True):
    __tablename__ = "infrastructure_cafo_manure_locations"

    cafo_manure_id: Optional[int] = Field(default=None, primary_key=True)
    latitude: Optional[Decimal] = Field(default=None)
    longitude: Optional[Decimal] = Field(default=None)
    owner_name: Optional[str] = Field(default=None)
    facility_name: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    town: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    animal: Optional[str] = Field(default=None)
    animal_feed_operation_type: Optional[str] = Field(default=None)
    animal_units: Optional[int] = Field(default=None)
    animal_count: Optional[int] = Field(default=None)
    manure_total_solids: Optional[Decimal] = Field(default=None)
    source: Optional[str] = Field(default=None)
    date_accessed: Optional[date] = Field(default=None)

