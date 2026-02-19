from ..base import BaseEntity
from datetime import date
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class Experiment(BaseEntity, table=True):
    __tablename__ = "experiment"

    analyst_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    exper_start_date: Optional[date] = Field(default=None)
    exper_duration: Optional[Decimal] = Field(default=None)
    exper_duration_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    exper_location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    description: Optional[str] = Field(default=None)

    # Relationships
    analyst: Optional["Contact"] = Relationship()
    exper_duration_unit: Optional["Unit"] = Relationship()
    exper_location: Optional["LocationAddress"] = Relationship()
