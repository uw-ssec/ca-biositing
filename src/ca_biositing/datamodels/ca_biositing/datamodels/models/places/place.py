from sqlmodel import Field, SQLModel
from typing import Optional


class Place(SQLModel, table=True):
    __tablename__ = "place"

    geoid: Optional[str] = Field(default=None, primary_key=True)
    state_name: Optional[str] = Field(default=None)
    state_fips: Optional[str] = Field(default=None)
    county_name: Optional[str] = Field(default=None)
    county_fips: Optional[str] = Field(default=None)
    region_name: Optional[str] = Field(default=None)
    agg_level_desc: Optional[str] = Field(default=None)
