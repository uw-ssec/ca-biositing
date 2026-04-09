from ..base import BaseEntity
from sqlmodel import Field, Relationship
from typing import Optional


class CountyAgReportRecord(BaseEntity, table=True):
    __tablename__ = "county_ag_report_record"

    record_id: str = Field(nullable=False, unique=True)
    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    primary_ag_product_id: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    description: Optional[str] = Field(default=None)
    resource_type: Optional[str] = Field(default=None)
    data_year: Optional[int] = Field(default=None)
    data_source_id: Optional[int] = Field(default=None, foreign_key="data_source.id")
    produced_nsjv: Optional[bool] = Field(default=None)
    processed_nsjv: Optional[bool] = Field(default=None)
    note: Optional[str] = Field(default=None)
    prodn_value_note: Optional[str] = Field(default=None)

    # Relationships
    place: Optional["Place"] = Relationship()
    primary_ag_product: Optional["PrimaryAgProduct"] = Relationship()
    data_source: Optional["DataSource"] = Relationship()
