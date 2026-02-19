from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class FieldStorageMethod(LookupBase, table=True):
    __tablename__ = "field_storage_method"
