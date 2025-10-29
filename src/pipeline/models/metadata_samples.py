from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Metadata(SQLModel, table=True):
    """Additional metadata linked to a field sample."""
    __tablename__ = "metadata"

    metadata_id: Optional[int] = Field(default=None, primary_key=True)
    sample_id: Optional[int] = Field(default=None,
                                     description="Reference to field_samples.sample_id")
                                     # foreign_key="field_samples.sample_id")
    ag_treatment_id: Optional[int] = Field(default=None,
                                           description="Reference to ag_treatments.ag_treatment_id")
                                           # foreign_key="ag_treatments.ag_treatment_id")
    last_application_date: Optional[date] = Field(default=None,
                                                  description="if applicable")
    treatment_amount_per_acre: Optional[Decimal] = Field(default=None,
                                                        description="if applicable")
    soil_type: Optional[int] = Field(default=None,
                                     description="Reference to soil_type.soil_type_id")
                                     # foreign_key="soil_type.soil_type_id")


class ParticleSize(SQLModel, table=True):
    """Particle‑size measurements for a sample."""
    __tablename__ = "particle_size"

    particle_size_id: Optional[int] = Field(default=None, primary_key=True)
    sample_id: Optional[int] = Field(default=None,
                                     description="Reference to field_samples.sample_id")
                                     # foreign_key="field_samples.sample_id")
    particle_length: Optional[int] = Field(default=None)
    particle_width: Optional[int] = Field(default=None)
    particle_height: Optional[int] = Field(default=None)
    particle_units: Optional[int] = Field(default=None,
                                          description="Reference to units.unit_id")
                                          # foreign_key="units.unit_id")


class SoilType(SQLModel, table=True):
    """Soil classification."""
    __tablename__ = "soil_type"

    soil_type_id: Optional[int] = Field(default=None, primary_key=True)
    soil_type: Optional[str] = Field(default=None, unique=True)
    soil_location: Optional[int] = Field(default=None,
                                         description="Reference to geographic_locations.location_id")
                                         # foreign_key="geographic_locations.location_id")


class AgTreatment(SQLModel, table=True):
    """Agricultural treatment (e.g., pesticide, herbicide)."""
    __tablename__ = "ag_treatments"

    ag_treatment_id: Optional[int] = Field(default=None, primary_key=True)
    ag_treatment_name: Optional[str] = Field(default=None,
                                              description="pesticide, herbicade")


class Taxonomy(SQLModel, table=True):
    """Taxonomic hierarchy for a biomass."""
    __tablename__ = "taxonomy"

    taxonomy_id: Optional[int] = Field(default=None, primary_key=True)
    kingdom: Optional[str] = Field(default=None)
    phylum: Optional[str] = Field(default=None)
    class_: Optional[str] = Field(default=None, alias="class")
    order: Optional[str] = Field(default=None)
    family: Optional[str] = Field(default=None)
    genus: Optional[str] = Field(default=None)
    species: Optional[str] = Field(default=None)
    variety_subspecies_cultivar: Optional[str] = Field(default=None)
