from ..base import Aim1RecordBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class XrfRecord(Aim1RecordBase, table=True):
    __tablename__ = "xrf_record"

    wavelength_nm: Optional[Decimal] = Field(default=None)
    intensity: Optional[Decimal] = Field(default=None)
    energy_slope: Optional[Decimal] = Field(default=None)
    energy_offset: Optional[Decimal] = Field(default=None)
