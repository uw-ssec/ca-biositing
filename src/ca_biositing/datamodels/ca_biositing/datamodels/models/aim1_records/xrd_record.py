from ..base import Aim1RecordBase
from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class XrdRecord(Aim1RecordBase, table=True):
    __tablename__ = "xrd_record"

    scan_low_nm: Optional[int] = Field(default=None)
    scan_high_nm: Optional[int] = Field(default=None)

