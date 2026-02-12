from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class CollectionMethod(LookupBase, table=True):
    __tablename__ = "collection_method"
