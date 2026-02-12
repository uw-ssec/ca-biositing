from ..base import BaseEntity, LookupBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class ParameterCategoryParameter(SQLModel, table=True):
    __tablename__ = "parameter_category_parameter"

    id: Optional[int] = Field(default=None, primary_key=True)
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameter.id")
    parameter_category_id: Optional[int] = Field(default=None, foreign_key="parameter_category.id")

    # Relationships
    parameter: Optional["Parameter"] = Relationship()
    parameter_category: Optional["ParameterCategory"] = Relationship()


class ParameterUnit(SQLModel, table=True):
    __tablename__ = "parameter_unit"

    id: Optional[int] = Field(default=None, primary_key=True)
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameter.id")
    alternate_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")

    # Relationships
    parameter: Optional["Parameter"] = Relationship()
    alternate_unit: Optional["Unit"] = Relationship()


class Parameter(BaseEntity, table=True):
    __tablename__ = "parameter"

    name: Optional[str] = Field(default=None)
    standard_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    calculated: Optional[bool] = Field(default=None)
    description: Optional[str] = Field(default=None)

    # Relationships
    standard_unit: Optional["Unit"] = Relationship()


class ParameterCategory(LookupBase, table=True):
    __tablename__ = "parameter_category"


