from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class LandiqResourceMapping(BaseEntity, table=True):
    __tablename__ = "landiq_resource_mapping"

    landiq_crop_name: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    resource_id: Optional[int] = Field(default=None, foreign_key="resource.id")

    # Relationships
    landiq_crop: Optional["PrimaryAgProduct"] = Relationship()
    resource: Optional["Resource"] = Relationship()

