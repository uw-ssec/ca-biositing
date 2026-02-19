from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class FtnirRecord(Aim1RecordBase, table=True):
    __tablename__ = "ftnir_record"
