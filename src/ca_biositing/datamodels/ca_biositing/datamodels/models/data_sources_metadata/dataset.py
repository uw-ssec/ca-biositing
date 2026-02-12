from ..base import BaseEntity
from datetime import date
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class Dataset(BaseEntity, table=True):
    __tablename__ = "dataset"

    name: Optional[str] = Field(default=None)
    record_type: Optional[str] = Field(default=None)
    source_id: Optional[int] = Field(default=None, foreign_key="data_source.id")
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    description: Optional[str] = Field(default=None)

    # Relationships
    source: Optional["DataSource"] = Relationship()

