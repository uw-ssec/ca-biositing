from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class CompositionalRecord(Aim1RecordBase, table=True):
    __tablename__ = "compositional_record"


