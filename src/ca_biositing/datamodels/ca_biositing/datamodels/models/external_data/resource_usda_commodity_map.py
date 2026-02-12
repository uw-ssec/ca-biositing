from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class ResourceUsdaCommodityMap(BaseEntity, table=True):
    __tablename__ = "resource_usda_commodity_map"

    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")
    primary_ag_product_id: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    usda_commodity_id: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")
    match_tier: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    resource: Optional["Resource"] = Relationship()
    primary_ag_product: Optional["PrimaryAgProduct"] = Relationship()
    usda_commodity: Optional["UsdaCommodity"] = Relationship()

