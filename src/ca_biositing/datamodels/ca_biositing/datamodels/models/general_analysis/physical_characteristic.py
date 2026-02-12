from ..base import BaseEntity
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class PhysicalCharacteristic(BaseEntity, table=True):
    __tablename__ = "physical_characteristic"

    field_sample_id: Optional[int] = Field(default=None, foreign_key="field_sample.id")
    particle_length: Optional[Decimal] = Field(default=None)
    particle_width: Optional[Decimal] = Field(default=None)
    particle_height: Optional[Decimal] = Field(default=None)
    particle_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")

    # Relationships
    field_sample: Optional["FieldSample"] = Relationship()
    particle_unit: Optional["Unit"] = Relationship()

