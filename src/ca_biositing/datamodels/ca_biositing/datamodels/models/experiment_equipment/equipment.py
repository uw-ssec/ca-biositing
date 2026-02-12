from ..base import LookupBase
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class Equipment(LookupBase, table=True):
    __tablename__ = "equipment"

    equipment_location_id: Optional[int] = Field(default=None, foreign_key="location_address.id")

    # Relationships
    equipment_location: Optional["LocationAddress"] = Relationship()

