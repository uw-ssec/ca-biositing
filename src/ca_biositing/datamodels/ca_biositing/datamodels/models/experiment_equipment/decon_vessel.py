from ..base import LookupBase
from sqlmodel import Field
from typing import Optional
from decimal import Decimal


class DeconVessel(LookupBase, table=True):
    __tablename__ = "decon_vessel"

    vessel_uuid: Optional[str] = Field(default=None, unique=True)
    serial_number: Optional[str] = Field(default=None)
    volume_numeric_per_well: Optional[Decimal] = Field(default=None)
    volume_unit: Optional[str] = Field(default=None)
