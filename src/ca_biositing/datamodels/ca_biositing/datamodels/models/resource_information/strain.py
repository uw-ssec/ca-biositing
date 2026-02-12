from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class Strain(LookupBase, table=True):
    __tablename__ = "strain"

    parent_strain_id: Optional[int] = Field(default=None)

