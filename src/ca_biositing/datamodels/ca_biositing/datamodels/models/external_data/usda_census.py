from ..base import BaseEntity, LookupBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class UsdaCommodity(LookupBase, table=True):
    __tablename__ = "usda_commodity"

    usda_source: Optional[str] = Field(default=None)
    usda_code: Optional[str] = Field(default=None)
    parent_commodity_id: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")

    # Relationships
    parent_commodity: Optional["UsdaCommodity"] = Relationship()


class UsdaCensusRecord(BaseEntity, table=True):
    __tablename__ = "usda_census_record"

    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    commodity_code: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")
    year: Optional[int] = Field(default=None)
    source_reference: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    dataset: Optional["Dataset"] = Relationship()
    place: Optional["Place"] = Relationship()
    commodity: Optional["UsdaCommodity"] = Relationship()


class UsdaDomain(LookupBase, table=True):
    __tablename__ = "usda_domain"



class UsdaStatisticCategory(LookupBase, table=True):
    __tablename__ = "usda_statistic_category"


