from ..base import BaseEntity, LookupBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class PreparationMethod(BaseEntity, table=True):
    __tablename__ = "preparation_method"

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    prep_method_abbrev_id: Optional[int] = Field(default=None, foreign_key="preparation_method_abbreviation.id")
    prep_temp_c: Optional[Decimal] = Field(default=None)
    uri: Optional[str] = Field(default=None)
    drying_step: Optional[bool] = Field(default=None)

    # Relationships
    prep_method_abbrev: Optional["PreparationMethodAbbreviation"] = Relationship()


class PreparationMethodAbbreviation(LookupBase, table=True):
    __tablename__ = "preparation_method_abbreviation"
