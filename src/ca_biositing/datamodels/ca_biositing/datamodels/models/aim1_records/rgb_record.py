from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class RgbRecord(Aim1RecordBase, table=True):
    __tablename__ = "rgb_record"
