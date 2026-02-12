from ..base import BaseEntity
from datetime import date
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class FieldSampleCondition(BaseEntity, table=True):
    __tablename__ = "field_sample_condition"

    field_sample_id: Optional[int] = Field(default=None, foreign_key="field_sample.id")
    ag_treatment_id: Optional[int] = Field(default=None, foreign_key="ag_treatment.id")
    last_application_date: Optional[date] = Field(default=None)
    treatment_amount_per_acre: Optional[float] = Field(default=None)
    processing_method_id: Optional[int] = Field(default=None, foreign_key="processing_method.id")

    # Relationships
    field_sample: Optional["FieldSample"] = Relationship()
    ag_treatment: Optional["AgTreatment"] = Relationship()
    processing_method: Optional["ProcessingMethod"] = Relationship()

