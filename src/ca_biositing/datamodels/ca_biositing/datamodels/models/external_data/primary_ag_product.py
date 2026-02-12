from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class PrimaryAgProduct(LookupBase, table=True):
    __tablename__ = "primary_ag_product"


