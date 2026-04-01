from ..base import Aim2RecordBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class GasificationRecord(Aim2RecordBase, table=True):
    __tablename__ = "gasification_record"

    # Feedstock mass, bed temperature, and gas flow rate removed as they are now stored as observations.
    reactor_type_id: Optional[int] = Field(default=None, foreign_key="decon_vessel.id")
