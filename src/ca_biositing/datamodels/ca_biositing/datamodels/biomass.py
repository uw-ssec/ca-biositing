from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


# ------------------------------------------------------------
# SQLModel classes generated from the DBdiagram schema
# ------------------------------------------------------------



# If you later want to add real FK constraints you can uncomment the import below
# from sqlalchemy import Column, Numeric, DateTime, func


# ----------------------------------------------------------------------
# Table: field_samples
# ----------------------------------------------------------------------
class FieldSample(SQLModel, table=True):
    """Sample metadata collected in the field."""
    __tablename__ = "field_samples"

    sample_id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for each sample",
    )
    biomass_id: int = Field(
        default=None,
        index=True,
        description="Reference to biomass"
        # foreign_key="biomass.biomass_id"
    )
    sample_name: str = Field(
        default=None,
        description='e.g., "Ene‑WaHu018"',
    )
    source_codename_id: Optional[int] = Field(
        default=None,
        index=True,
        description="Anonymized source identifier",
    )
    data_source_id: Optional[int] = Field(
        default=None,
        description="Reference to data source"
        # foreign_key="data_sources.source_id"
    )
    location_id: Optional[int] = Field(
        default=None,
        description="Reference to geographic location (may be null)"
        # foreign_key="geographic_locations.location_id"
    )
    field_storage_id: Optional[int] = Field(
        default=None,
        description="Reference to field storage"
        # foreign_key="field_storage.field_storage_id"
    )
    field_storage_duration_value: Optional[Decimal] = Field(
        default=None,
        description="Duration value for field storage",
    )
    field_storage_duration_unit_id: Optional[int] = Field(
        default=None,
        description="Reference to unit of storage duration"
        # foreign_key="units.unit_id"
    )
    collection_timestamp: Optional[datetime] = Field(default=None)
    collection_method_id: Optional[int] = Field(
        default=None,
        description="Reference to collection method"
        # foreign_key="collection_methods.collection_method_id"
    )
    harvest_method_id: Optional[int] = Field(
        default=None,
        description="Reference to harvest method"
        # foreign_key="harvest_methods.harvest_method_id"
    )
    harvest_date: Optional[date] = Field(default=None)
    amount_collected_kg: Optional[Decimal] = Field(default=None)
    provider_id: Optional[int] = Field(
        default=None,
        description="Reference to provider (anonymized)"
        # foreign_key="providers.provider_id"
    )
    collector_id: Optional[int] = Field(
        default=None,
        description="Reference to collector"
        # foreign_key="collectors.collector_id"
    )
    basic_sample_info_note: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the record was created",
    )


# ----------------------------------------------------------------------
# Table: biomass
# ----------------------------------------------------------------------
class Biomass(SQLModel, table=True):
    """Core biomass entity."""
    __tablename__ = "biomass"

    biomass_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_name: str = Field(default=None, index=True)
    primary_product_id: Optional[int] = Field(
        default=None,
        description="Reference to primary product"
        # foreign_key="primary_product.primary_product_id"
    )
    taxonomy_id: Optional[int] = Field(
        default=None,
        description="Reference to taxonomy"
        # foreign_key="taxonomy.taxonomy_id"
    )
    biomass_type_id: Optional[int] = Field(
        default=None,
        index=True,
        description="Reference to biomass type"
        # foreign_key="biomass_type.biomass_type_id"
    )
    biomass_notes: Optional[str] = Field(default=None)


# ----------------------------------------------------------------------
# Table: biomass_test
# ----------------------------------------------------------------------

class BiomassTest(SQLModel, table=True):
    """Testing Table"""
    __tablename__ = "biomass_test"

    biomass_test_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_test_name: str = Field(default=None, index=True)
    biomass_test_notes: Optional[str] = Field(default=None)



# ----------------------------------------------------------------------
# Table: biomass_type
# ----------------------------------------------------------------------
class BiomassType(SQLModel, table=True):
    """Lookup table for biomass type (e.g., crop by‑product, wood residue)."""
    __tablename__ = "biomass_type"

    biomass_type_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_type: str = Field(
        default=None,
        unique=True,
        description="Crop by‑product, Wood residue, etc.",
    )


# ----------------------------------------------------------------------
# Table: primary_product
# ----------------------------------------------------------------------
class PrimaryProduct(SQLModel, table=True):
    """Lookup table for primary products derived from biomass."""
    __tablename__ = "primary_product"

    primary_product_id: Optional[int] = Field(default=None, primary_key=True)
    primary_product_name: str = Field(default=None, unique=True)


# ----------------------------------------------------------------------
# Table: biomass_availability
# ----------------------------------------------------------------------
class BiomassAvailability(SQLModel, table=True):
    """Seasonal and quantitative availability of a biomass."""
    __tablename__ = "biomass_availability"

    availability_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_id: int = Field(
        default=None,
        index=True,
        description="Reference to biomass"
        # foreign_key="biomass.biomass_id"
    )
    location_id: Optional[int] = Field(
        default=None,
        description="Reference to geographic location"
        # foreign_key="geographic_locations.location_id"
    )
    primary_product_id: Optional[int] = Field(
        default=None,
        description="Reference to primary product"
        # foreign_key="primary_product.primary_product_id"
    )
    from_month: Optional[Decimal] = Field(
        default=None,
        description="Start month (e.g. 1 = Jan, 6.5 = mid‑June)",
    )
    to_month: Optional[Decimal] = Field(
        default=None,
        description="End month (e.g. 12 = Dec)",
    )
    kg_low: Optional[Decimal] = Field(default=None, description="Annual low estimate (kg)")
    kg_avg: Optional[Decimal] = Field(default=None, description="Annual average estimate (kg)")
    kg_high: Optional[Decimal] = Field(default=None, description="Annual high estimate (kg)")
    bdt_low: Optional[Decimal] = Field(default=None, description="Bone‑dry tons low estimate")
    bdt_avg: Optional[Decimal] = Field(default=None, description="Bone‑dry tons average")
    bdt_high: Optional[Decimal] = Field(default=None, description="Bone‑dry tons high estimate")
    data_source: Optional[int] = Field(
        default=None,
        description="Reference to data source"
        # foreign_key="data_sources.source_id"
    )
    availability_notes: Optional[str] = Field(default=None)


# ----------------------------------------------------------------------
# Table: biomass_quality
# ----------------------------------------------------------------------
class BiomassQuality(SQLModel, table=True):
    """Qualitative attributes of a biomass."""
    __tablename__ = "biomass_quality"

    quality_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_id: int = Field(
        default=None,
        index=True,
        description="Reference to biomass"
        # foreign_key="biomass.biomass_id"
    )
    expected_quality: Optional[str] = Field(default=None)
    output_feedstocks: Optional[str] = Field(
        default=None,
        description="(Optional) Output feedstocks – may be moved to another table",
    )
    convertibility: Optional[str] = Field(default=None)
    disposal_challenges: Optional[str] = Field(
        default=None,
        description="Nondisposability issues",
    )
    existing_markets: Optional[str] = Field(
        default=None,
        description="Substitutability information",
    )
    substitute_materials: Optional[str] = Field(default=None)
    regulatory_issues: Optional[str] = Field(default=None)
    quality_data_sources: Optional[int] = Field(
        default=None,
        description="Reference to data source"
        # foreign_key="data_sources.source_id"
    )
    notes: Optional[str] = Field(default=None)


# ----------------------------------------------------------------------
# Table: biomass_price
# ----------------------------------------------------------------------
class BiomassPrice(SQLModel, table=True):
    """Pricing information for a biomass."""
    __tablename__ = "biomass_price"

    price_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_id: int = Field(
        default=None,
        index=True,
        description="Reference to biomass"
        # foreign_key="biomass.biomass_id"
    )
    price_per_kg_low: Optional[Decimal] = Field(default=None)
    price_per_kg_avg: Optional[Decimal] = Field(default=None)
    price_per_kg_high: Optional[Decimal] = Field(default=None)
    price_data_sources: Optional[int] = Field(
        default=None,
        description="Reference to data source"
        # foreign_key="data_sources.source_id"
    )
    notes: Optional[str] = Field(default=None)

# ----------------------------------------------------------------------
# Table: harvest_methods
# ----------------------------------------------------------------------
class HarvestMethod(SQLModel, table=True):
    """Lookup table for harvest methods."""
    __tablename__ = "harvest_methods"

    harvest_method_id: Optional[int] = Field(default=None, primary_key=True)
    harvest_method_name: str = Field(default=None, unique=True)

# ----------------------------------------------------------------------
# Table: collection_methods
# ----------------------------------------------------------------------
class CollectionMethod(SQLModel, table=True):
    """Lookup table for collection methods."""
    __tablename__ = "collection_methods"

    collection_method_id: Optional[int] = Field(default=None, primary_key=True)
    collection_method_name: str = Field(default=None, unique=True)

# ----------------------------------------------------------------------
# Table: field_storage
# ----------------------------------------------------------------------
class FieldStorage(SQLModel, table=True):
    """Lookup table for field storage methods."""
    __tablename__ = "field_storage"

    field_storage_id: Optional[int] = Field(default=None, primary_key=True)
    storage_method: str = Field(default=None, unique=True)
