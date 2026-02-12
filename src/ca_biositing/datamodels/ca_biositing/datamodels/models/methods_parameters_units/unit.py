from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class Unit(LookupBase, table=True):
    __tablename__ = "unit"
