"""
Base mixin classes for SQLModel models.

These are non-table mixins that provide shared fields to entity tables.
They replace the concrete BaseEntity and LookupBase tables from the LinkML-generated code.
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class BaseEntity(SQLModel):
    """
    Mixin for all main entity tables. Provides id, timestamps, lineage.

    This is NOT a table itself - it's a mixin that child classes inherit from.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    etl_run_id: Optional[int] = Field(default=None, foreign_key="etl_run.id")
    lineage_group_id: Optional[int] = Field(default=None)


class LookupBase(SQLModel):
    """
    Mixin for enum/ontology-like lookup tables. Provides id, name, description, uri.

    This is NOT a table itself - it's a mixin that child classes inherit from.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    uri: Optional[str] = Field(default=None)


class Aim1RecordBase(BaseEntity):
    """
    Mixin for Aim1 analytical records. Adds record_id + common experiment/sample fields.

    Inherits from BaseEntity, so also includes id, timestamps, and lineage fields.
    """
    record_id: str = Field(nullable=False, unique=True)
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    prepared_sample_id: Optional[int] = Field(default=None, foreign_key="prepared_sample.id")
    technical_replicate_no: Optional[int] = Field(default=None)
    technical_replicate_total: Optional[int] = Field(default=None)
    method_id: Optional[int] = Field(default=None, foreign_key="method.id")
    analyst_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    raw_data_id: Optional[int] = Field(default=None, foreign_key="file_object_metadata.id")
    qc_pass: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)


class Aim2RecordBase(BaseEntity):
    """
    Mixin for Aim2 processing records. Adds record_id + common experiment/sample fields.

    Inherits from BaseEntity, so also includes id, timestamps, and lineage fields.
    """
    record_id: str = Field(nullable=False, unique=True)
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    prepared_sample_id: Optional[int] = Field(default=None, foreign_key="prepared_sample.id")
    technical_replicate_no: Optional[int] = Field(default=None)
    technical_replicate_total: Optional[int] = Field(default=None)
    method_id: Optional[int] = Field(default=None, foreign_key="method.id")
    analyst_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    raw_data_id: Optional[int] = Field(default=None, foreign_key="file_object_metadata.id")
    qc_pass: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)
