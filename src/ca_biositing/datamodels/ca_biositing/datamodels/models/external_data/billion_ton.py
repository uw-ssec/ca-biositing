from ..base import BaseEntity
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class BillionTon2023Record(BaseEntity, table=True):
    __tablename__ = "billion_ton2023_record"

    subclass_id: Optional[int] = Field(default=None, foreign_key="resource_subclass.id")
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    county_square_miles: Optional[float] = Field(default=None)
    model_name: Optional[str] = Field(default=None)
    scenario_name: Optional[str] = Field(default=None)
    price_offered_usd: Optional[Decimal] = Field(default=None)
    production: Optional[int] = Field(default=None)
    production_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    btu_ton: Optional[int] = Field(default=None)
    production_energy_content: Optional[int] = Field(default=None)
    energy_content_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    product_density_dtpersqmi: Optional[Decimal] = Field(default=None)
    land_source: Optional[str] = Field(default=None)

    # Relationships
    subclass: Optional["ResourceSubclass"] = Relationship()
    resource: Optional["Resource"] = Relationship()
    place: Optional["Place"] = Relationship()
    production_unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[BillionTon2023Record.production_unit_id]"}
    )
    energy_content_unit: Optional["Unit"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[BillionTon2023Record.energy_content_unit_id]"}
    )
