from ..base import BaseEntity
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional


class Observation(BaseEntity, table=True):
    __tablename__ = "observation"
    __table_args__ = (
        UniqueConstraint(
            'record_id', 'record_type', 'parameter_id', 'unit_id',
            name='observation_unique_key'
        ),
    )

    record_id: str = Field(nullable=False)
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    record_type: Optional[str] = Field(default=None)
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameter.id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    dimension_type_id: Optional[int] = Field(default=None, foreign_key="dimension_type.id")
    dimension_value: Optional[Decimal] = Field(default=None)
    dimension_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    note: Optional[str] = Field(default=None)

    # Relationships
    dataset: Optional["Dataset"] = Relationship()
    parameter: Optional["Parameter"] = Relationship()
    unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Observation.unit_id]"}
    )
    dimension_type: Optional["DimensionType"] = Relationship()
    dimension_unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Observation.dimension_unit_id]"}
    )
