from ..base import Aim2RecordBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class GasificationRecord(Aim2RecordBase, table=True):
    __tablename__ = "gasification_record"

    feedstock_mass: Optional[Decimal] = Field(default=None)
    bed_temperature: Optional[Decimal] = Field(default=None)
    gas_flow_rate: Optional[Decimal] = Field(default=None)

