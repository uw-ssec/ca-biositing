from ..base import BaseEntity, LookupBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class DataSource(BaseEntity, table=True):
    __tablename__ = "data_source"

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    data_source_type_id: Optional[int] = Field(default=None, foreign_key="data_source_type.id")
    full_title: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)
    subject: Optional[str] = Field(default=None)
    publisher: Optional[str] = Field(default=None)
    contributor: Optional[str] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    type: Optional[str] = Field(default=None)
    biocirv: Optional[bool] = Field(default=None)
    format: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    relation: Optional[str] = Field(default=None)
    temporal_coverage: Optional[str] = Field(default=None)
    location_coverage_id: Optional[int] = Field(default=None, foreign_key="location_resolution.id")
    rights: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    uri: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    data_source_type: Optional["DataSourceType"] = Relationship()
    location_coverage: Optional["LocationResolution"] = Relationship()


class DataSourceType(BaseEntity, table=True):
    __tablename__ = "data_source_type"

    source_type_id: Optional[int] = Field(default=None, foreign_key="source_type.id")

    # Relationships
    source_type: Optional["SourceType"] = Relationship()


class SourceType(LookupBase, table=True):
    __tablename__ = "source_type"
