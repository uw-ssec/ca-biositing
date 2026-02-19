from sqlmodel import Field, SQLModel
from typing import Optional


class InfrastructureEthanolBiorefineries(SQLModel, table=True):
    __tablename__ = "infrastructure_ethanol_biorefineries"

    ethanol_biorefinery_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    capacity_mgy: Optional[int] = Field(default=None)
    production_mgy: Optional[int] = Field(default=None)
    constr_exp: Optional[int] = Field(default=None)
