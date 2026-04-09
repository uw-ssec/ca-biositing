from ..base import BaseEntity
from sqlmodel import Field, Relationship
from typing import Optional
from sqlalchemy import UniqueConstraint


class ResourceImage(BaseEntity, table=True):
    __tablename__ = "resource_image"
    __table_args__ = (
        UniqueConstraint('resource_id', 'image_url', name='resource_image_resource_id_image_url_key'),
    )

    resource_id: int = Field(foreign_key="resource.id")
    resource_name: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    sort_order: Optional[int] = Field(default=None)

    # Relationships
    resource: Optional["Resource"] = Relationship()
