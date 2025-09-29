from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


# ----------------------------------------------------------------------
# Organizational tables
# ----------------------------------------------------------------------


class Affiliation(SQLModel, table=True):
    """Affiliation (e.g., university, company)."""
    __tablename__ = "affiliations"

    affiliation_id: Optional[int] = Field(default=None, primary_key=True)
    affiliation_name: str = Field(..., unique=True, description="Not null")


class Building(SQLModel, table=True):
    """Building that can house rooms / equipment."""
    __tablename__ = "buildings"

    building_id: Optional[int] = Field(default=None, primary_key=True)
    building_name: Optional[str] = Field(default=None, unique=True)
    location_id: Optional[int] = Field(default=None,
                                       description="Reference to geographic_locations.location_id",
                                       foreign_key="geographic_locations.location_id")
    affiliation_id: Optional[int] = Field(default=None,
                                         description="Reference to affiliations.affiliation_id",
                                         foreign_key="affiliations.affiliation_id")


class Room(SQLModel, table=True):
    """Room inside a building."""
    __tablename__ = "rooms"

    room_id: Optional[int] = Field(default=None, primary_key=True)
    room_number: Optional[str] = Field(default=None, unique=True)
    building_id: Optional[int] = Field(default=None,
                                       description="Reference to buildings.building_id",
                                       foreign_key="buildings.building_id")
