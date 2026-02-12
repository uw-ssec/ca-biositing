from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class Contact(BaseEntity, table=True):
    __tablename__ = "contact"

    name: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    affiliation: Optional[str] = Field(default=None)

