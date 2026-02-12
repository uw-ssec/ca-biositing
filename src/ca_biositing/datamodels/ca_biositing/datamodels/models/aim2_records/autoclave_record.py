from ..base import Aim2RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class AutoclaveRecord(Aim2RecordBase, table=True):
    __tablename__ = "autoclave_record"


