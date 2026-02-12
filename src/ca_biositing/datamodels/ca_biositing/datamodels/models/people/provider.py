from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class Provider(BaseEntity, table=True):
    __tablename__ = "provider"

    codename: Optional[str] = Field(default=None)
