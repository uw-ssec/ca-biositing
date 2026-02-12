from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Index, text
from geoalchemy2 import Geometry
from typing import Any, Optional


class Polygon(BaseEntity, table=True):
    """Geographic polygon with MD5-based unique constraint on geometry."""
    __tablename__ = "polygon"
    __table_args__ = (
        Index('unique_geom_dataset_md5', text('md5(geom::text)'), 'dataset_id', unique=True),
    )

    geoid: Optional[str] = Field(default=None)
    geom: Optional[Any] = Field(default=None, sa_column=Column(Geometry(spatial_index=False)))
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")

    # Relationships
    dataset: Optional["Dataset"] = Relationship()

