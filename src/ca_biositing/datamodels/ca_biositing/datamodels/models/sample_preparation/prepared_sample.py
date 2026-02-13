from ..base import BaseEntity
from datetime import date
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class PreparedSample(BaseEntity, table=True):
    __tablename__ = "prepared_sample"

    name: Optional[str] = Field(default=None)
    field_sample_id: Optional[int] = Field(default=None, foreign_key="field_sample.id")
    prep_method_id: Optional[int] = Field(default=None, foreign_key="preparation_method.id")
    prep_date: Optional[date] = Field(default=None)
    preparer_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    note: Optional[str] = Field(default=None)

    # Relationships
    field_sample: Optional["FieldSample"] = Relationship()
    prep_method: Optional["PreparationMethod"] = Relationship()
    preparer: Optional["Contact"] = Relationship()
