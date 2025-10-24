from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# Sample preprocessing / processing
# ----------------------------------------------------------------------


class PreprocessingMethod(SQLModel, table=True):
    """Method used to pre‑process a sample."""
    __tablename__ = "preprocessing_methods"

    prepro_method_id: Optional[int] = Field(default=None, primary_key=True)
    prepro_method: Optional[str] = Field(default=None,
                                          description="As Is, Knife Mill (2mm), Oven Dry")
    prepro_method_abbrev_id: Optional[int] = Field(default=None,
                                                   description="Reference to preprocessing_methods_abbreviations.prepro_methods_abbrev_id",)
                                                   # foreign_key="preprocessing_methods_abbreviations.prepro_methods_abbrev_id")
    prepro_temp_c: Optional[Decimal] = Field(default=None)
    drying_step: Optional[bool] = Field(default=None)
    method_ref_id: Optional[int] = Field(default=None,
                                         description="Reference to references.reference_id",)
                                         # foreign_key="references.reference_id")


class PreprocessingMethodAbbreviation(SQLModel, table=True):
    """Abbreviation for a preprocessing method."""
    __tablename__ = "preprocessing_methods_abbreviations"

    prepro_methods_abbrev_id: Optional[int] = Field(default=None, primary_key=True)
    prepro_method_abbrev: Optional[str] = Field(default=None, unique=True)


class PreprocessedSample(SQLModel, table=True):
    """Result of a preprocessing step."""
    __tablename__ = "preprocessed_samples"

    prepro_material_id: Optional[int] = Field(default=None, primary_key=True)
    prepro_material_name: Optional[str] = Field(default=None)
    biomass_sample_id: Optional[int] = Field(default=None,
                                             description="Reference to field_samples.sample_id",)
                                             # foreign_key="field_samples.sample_id")
    prepro_method_id: Optional[int] = Field(default=None,
                                            description="Reference to preprocessing_methods.prepro_method_id",)
                                            # foreign_key="preprocessing_methods.prepro_method_id")
    amount_before_drying_g: Optional[Decimal] = Field(default=None)
    amount_after_drying: Optional[Decimal] = Field(default=None)
    processing_date: Optional[date] = Field(default=None)
    storage_building: Optional[int] = Field(default=None,
                                            description="Reference to buildings.building_id",)
                                            # foreign_key="buildings.building_id")
    amount_remaining_g: Optional[Decimal] = Field(default=None)
    amount_as_of_date: Optional[date] = Field(default=None)
    prepro_analyst_id: Optional[int] = Field(default=None,
                                              description="Reference to analyst_contact.analyst_id",)
                                              # foreign_key="analyst_contact.analyst_id")
    prepro_note: Optional[str] = Field(default=None)

    __table_args__ = (
        Index("idx_preprocessed_samples_biomass_sample_id", "biomass_sample_id"),
        Index("idx_preprocessed_samples_prepro_method_id", "prepro_method_id"),
    )
