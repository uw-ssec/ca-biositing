from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class LandiqRecord(BaseEntity, table=True):
    __tablename__ = "landiq_record"

    record_id: str = Field(unique=True, nullable=False)
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    polygon_id: Optional[int] = Field(default=None, foreign_key="polygon.id")
    main_crop: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    secondary_crop: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    tertiary_crop: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    quaternary_crop: Optional[int] = Field(default=None, foreign_key="primary_ag_product.id")
    confidence: Optional[int] = Field(default=None)
    irrigated: Optional[bool] = Field(default=None)
    acres: Optional[float] = Field(default=None)
    county: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)
    pct1: Optional[float] = Field(default=None)
    pct2: Optional[float] = Field(default=None)
    pct3: Optional[float] = Field(default=None)
    pct4: Optional[float] = Field(default=None)

    # Relationships
    polygon: Optional["Polygon"] = Relationship()
    dataset: Optional["Dataset"] = Relationship()
    main_crop_product: Optional["PrimaryAgProduct"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LandiqRecord.main_crop]"}
    )
    secondary_crop_product: Optional["PrimaryAgProduct"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LandiqRecord.secondary_crop]"}
    )
    tertiary_crop_product: Optional["PrimaryAgProduct"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LandiqRecord.tertiary_crop]"}
    )
    quaternary_crop_product: Optional["PrimaryAgProduct"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LandiqRecord.quaternary_crop]"}
    )
