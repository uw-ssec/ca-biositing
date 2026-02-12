from ..base import BaseEntity
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class FacilityRecord(BaseEntity, table=True):
    __tablename__ = "facility_record"

    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    facility_name: Optional[str] = Field(default=None)
    location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    capacity_mw: Optional[Decimal] = Field(default=None)
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    operator: Optional[str] = Field(default=None)
    start_year: Optional[int] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    dataset: Optional["Dataset"] = Relationship()
    location: Optional["LocationAddress"] = Relationship()
    resource: Optional["Resource"] = Relationship()

