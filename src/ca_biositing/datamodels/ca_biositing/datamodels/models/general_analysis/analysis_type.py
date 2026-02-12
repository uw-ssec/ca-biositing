from ..base import LookupBase
from sqlmodel import Field, SQLModel
from typing import Optional


class AnalysisType(LookupBase, table=True):
    __tablename__ = "analysis_type"


