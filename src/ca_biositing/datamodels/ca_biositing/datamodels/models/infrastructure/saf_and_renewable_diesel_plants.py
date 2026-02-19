from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class InfrastructureSafAndRenewableDieselPlants(SQLModel, table=True):
    __tablename__ = "infrastructure_saf_and_renewable_diesel_plants"

    ibcc_index: Optional[int] = Field(default=None, primary_key=True)
    company: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    capacity: Optional[str] = Field(default=None)
    feedstock: Optional[str] = Field(default=None)
    products: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    coordinates: Optional[str] = Field(default=None)
    latitude: Optional[Decimal] = Field(default=None)
    longitude: Optional[Decimal] = Field(default=None)
