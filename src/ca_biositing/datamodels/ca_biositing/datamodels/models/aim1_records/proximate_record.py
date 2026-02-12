from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class ProximateRecord(Aim1RecordBase, table=True):
    __tablename__ = "proximate_record"


