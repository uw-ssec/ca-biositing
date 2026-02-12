from ..base import BaseEntity
from datetime import date
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class FieldSample(BaseEntity, table=True):
    __tablename__ = "field_sample"

    name: Optional[str] = Field(default=None)
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    collector_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    sample_collection_source: Optional[str] = Field(default=None)
    amount_collected: Optional[Decimal] = Field(default=None)
    amount_collected_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    sampling_location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    field_storage_method_id: Optional[int] = Field(default=None, foreign_key="field_storage_method.id")
    field_storage_duration_value: Optional[Decimal] = Field(default=None)
    field_storage_duration_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    field_storage_location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    collection_timestamp: Optional[datetime] = Field(default=None)
    collection_method_id: Optional[int] = Field(default=None, foreign_key="collection_method.id")
    harvest_method_id: Optional[int] = Field(default=None, foreign_key="harvest_method.id")
    harvest_date: Optional[date] = Field(default=None)
    field_sample_storage_location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    note: Optional[str] = Field(default=None)

    # Relationships
    resource: Optional["Resource"] = Relationship()
    provider: Optional["Provider"] = Relationship()
    collector: Optional["Contact"] = Relationship()
    amount_collected_unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[FieldSample.amount_collected_unit_id]"}
    )
    sampling_location: Optional["LocationAddress"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[FieldSample.sampling_location_id]"}
    )
    field_storage_method: Optional["FieldStorageMethod"] = Relationship()
    field_storage_duration_unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[FieldSample.field_storage_duration_unit_id]"}
    )
    field_storage_location: Optional["LocationAddress"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[FieldSample.field_storage_location_id]"}
    )
    collection_method: Optional["CollectionMethod"] = Relationship()
    harvest_method: Optional["HarvestMethod"] = Relationship()
    field_sample_storage_location: Optional["LocationAddress"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[FieldSample.field_sample_storage_location_id]"}
    )

