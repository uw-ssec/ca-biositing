from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class AgTreatment(LookupBase, table=True):
    __tablename__ = "ag_treatment"
