from decimal import Decimal
from sqlmodel import Field, SQLModel
from typing import Optional


class InfrastructureMswToEnergyAnaerobicDigesters(SQLModel, table=True):
    __tablename__ = "infrastructure_msw_to_energy_anaerobic_digesters"

    wte_id: Optional[int] = Field(default=None, primary_key=True)
    city: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    equivalent_generation: Optional[Decimal] = Field(default=None)
    feedstock: Optional[str] = Field(default=None)
    dayload: Optional[Decimal] = Field(default=None)
    dayload_bdt: Optional[Decimal] = Field(default=None)
    facility_type: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    wkt_geom: Optional[str] = Field(default=None)
    geom: Optional[str] = Field(default=None)
    latitude: Optional[Decimal] = Field(default=None)
    longitude: Optional[Decimal] = Field(default=None)


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


class InfrastructureWastewaterTreatmentPlants(SQLModel, table=True):
    __tablename__ = "infrastructure_wastewater_treatment_plants"

    plant_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    codigestion: Optional[str] = Field(default=None)
    flow_design_adjusted: Optional[Decimal] = Field(default=None)
    flow_average: Optional[Decimal] = Field(default=None)
    biosolids: Optional[Decimal] = Field(default=None)
    excess_flow: Optional[Decimal] = Field(default=None)
    biogas_utilized: Optional[bool] = Field(default=None)
    flaring: Optional[bool] = Field(default=None)
    excess_mass_loading_rate: Optional[Decimal] = Field(default=None)
    excess_mass_loading_rate_wet: Optional[Decimal] = Field(default=None)
    methane_production: Optional[Decimal] = Field(default=None)
    energy_content: Optional[Decimal] = Field(default=None)
    electric_kw: Optional[Decimal] = Field(default=None)
    thermal_mmbtu_d: Optional[Decimal] = Field(default=None)
    electric_kwh: Optional[Decimal] = Field(default=None)
    thermal_annual_mmbtu_y: Optional[Decimal] = Field(default=None)
    anaerobic_digestion_facility: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    dayload_bdt: Optional[Decimal] = Field(default=None)
    dayload: Optional[Decimal] = Field(default=None)
    equivalent_generation: Optional[Decimal] = Field(default=None)
    facility_type: Optional[str] = Field(default=None)
    feedstock: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    latitude: Optional[Decimal] = Field(default=None)
    longitude: Optional[Decimal] = Field(default=None)
    zipcode: Optional[str] = Field(default=None)
