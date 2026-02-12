from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class DimensionType(LookupBase, table=True):
    __tablename__ = "dimension_type"
