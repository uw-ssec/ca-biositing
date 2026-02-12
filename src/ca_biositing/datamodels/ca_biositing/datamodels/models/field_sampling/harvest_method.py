from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class HarvestMethod(LookupBase, table=True):
    __tablename__ = "harvest_method"


