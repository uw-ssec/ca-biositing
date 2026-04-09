from ..base import BaseEntity
from sqlmodel import Field, Relationship
from typing import Optional


class ResourceImage(BaseEntity, table=True):
    __tablename__ = "resource_image"

    resource_id: int = Field(foreign_key="resource.id")
    resource_name: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    sort_order: Optional[int] = Field(default=None)

    # Relationships
    resource: Optional["Resource"] = Relationship()
