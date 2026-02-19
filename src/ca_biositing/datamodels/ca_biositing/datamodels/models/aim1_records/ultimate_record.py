from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class UltimateRecord(Aim1RecordBase, table=True):
    __tablename__ = "ultimate_record"
