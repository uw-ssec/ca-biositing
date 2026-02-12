from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class ProcessingMethod(LookupBase, table=True):
    __tablename__ = "processing_method"


