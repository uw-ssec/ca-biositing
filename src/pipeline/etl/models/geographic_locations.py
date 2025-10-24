from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# Geographic / Location tables
# ----------------------------------------------------------------------


class GeographicLocation(SQLModel, table=True):
    """Geographic location (can be anonymised)."""
    __tablename__ = "geographic_locations"

    location_id: Optional[int] = Field(default=None, primary_key=True)
    street_address_id: Optional[int] = Field(default=None,
                                             description="Reference to street_addresses.street_address_id")
                                             # foreign_key="street_addresses.street_address_id")
    city_id: Optional[int] = Field(default=None,
                                    description="Reference to cities.city_id")
                                    # foreign_key="cities.city_id")
    zip_id: Optional[int] = Field(default=None,
                                   description="Reference to zips.zip_id")
                                   # foreign_key="zips.zip_id")
    county_id: Optional[int] = Field(default=None,
                                     description="Reference to counties.county_id")
                                     # foreign_key="counties.county_id")
    state_id: Optional[int] = Field(default=None,
                                    description="Reference to states.state_id")
                                    # foreign_key="states.state_id")
    region_id: Optional[int] = Field(default=None,
                                     description="Reference to regions.region_id")
                                     # foreign_key="regions.region_id")
    fips_id: Optional[int] = Field(default=None,
                                    description="Reference to fips.fips_id")
                                    # foreign_key="fips.fips_id")
    latitude: Optional[Decimal] = Field(default=None,
                                         description="Can be null or generalized")
    longitude: Optional[Decimal] = Field(default=None,
                                          description="Can be null or generalized")
    location_resolution_id: Optional[int] = Field(default=None,
                                                 description="Reference to location_resolutions.location_resolution_id")
                                                 # foreign_key="location_resolutions.location_resolution_id")
    is_anonymous: Optional[bool] = Field(default=None)


class StreetAddress(SQLModel, table=True):
    """Street address (may be null for privacy)."""
    __tablename__ = "street_addresses"

    street_address_id: Optional[int] = Field(default=None, primary_key=True)
    street_address: str = Field(..., description="Not null")


class City(SQLModel, table=True):
    """City lookup."""
    __tablename__ = "cities"

    city_id: Optional[int] = Field(default=None, primary_key=True)
    city_name: str = Field(..., unique=True, description="Not null")


class Zip(SQLModel, table=True):
    """ZIP code lookup."""
    __tablename__ = "zips"

    zip_id: Optional[int] = Field(default=None, primary_key=True)
    zip_code: str = Field(..., unique=True, description="Not null")


class County(SQLModel, table=True):
    """County lookup."""
    __tablename__ = "counties"

    county_id: Optional[int] = Field(default=None, primary_key=True)
    county_name: str = Field(..., unique=True, description="Not null")


class FIPS(SQLModel, table=True):
    """FIPS code (preserve leading zeros)."""
    __tablename__ = "fips"

    fips_id: Optional[int] = Field(default=None, primary_key=True)
    fips_description: Optional[str] = Field(default=None)


class State(SQLModel, table=True):
    """State lookup."""
    __tablename__ = "states"

    state_id: Optional[int] = Field(default=None, primary_key=True)
    state_name: str = Field(..., unique=True, description="Not null")


class Region(SQLModel, table=True):
    """Region lookup."""
    __tablename__ = "regions"

    region_id: Optional[int] = Field(default=None, primary_key=-1)
    region_name: str = Field(..., unique=True, description="Not null")


class LocationResolution(SQLModel, table=True):
    """Resolution of a location (e.g., GPS, county, state)."""
    __tablename__ = "location_resolutions"

    location_resolution_id: Optional[int] = Field(default=None, primary_key=True)
    resolution_type: str = Field(..., unique=True,
                                 description="region, state, city, county, etc")
