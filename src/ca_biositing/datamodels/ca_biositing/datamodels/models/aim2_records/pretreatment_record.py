from ..base import Aim2RecordBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class PretreatmentRecord(Aim2RecordBase, table=True):
    __tablename__ = "pretreatment_record"

    pretreatment_method_id: Optional[int] = Field(default=None)
    eh_method_id: Optional[int] = Field(default=None)
    reaction_block_id: Optional[int] = Field(default=None)
    block_position: Optional[str] = Field(default=None)
    temperature: Optional[Decimal] = Field(default=None)
    replicate_no: Optional[int] = Field(default=None)
