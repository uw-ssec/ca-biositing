from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# Specific analysis result tables
# ----------------------------------------------------------------------


class ProximateAnalysis(SQLModel, table=True):
    """Proximate analysis results (e.g., moisture, ash)."""
    __tablename__ = "proximate_analysis"

    prox_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    notes: Optional[str] = Field(default=None)


class ICPAnalysis(SQLModel, table=True):
    """ICP (Inductively Coupled Plasma) analysis."""
    __tablename__ = "icp_analysis"

    icp_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    concentration_calculation_url_id: Optional[int] = Field(default=None,
                                                          description="Reference to url.url_id",
                                                          foreign_key="url.url_id")
    result_wavelength: Optional[Decimal] = Field(default=None)
    raw_url: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class CompositionalAnalysis(SQLModel, table=True):
    """Compositional analysis (derived parameters)."""
    __tablename__ = "compositional_analysis"

    cmp_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    calculated_parameter_id: Optional[int] = Field(default=None,
                                                  description="Reference to parameters.parameter_id",
                                                  foreign_key="parameters.parameter_id")
    calculated_parameter_value: Optional[Decimal] = Field(default=None)
    calculated_parameter_unit_id: Optional[int] = Field(default=None,
                                                       description="Reference to units.unit_id",
                                                       foreign_key="units.unit_id")
    notes: Optional[str] = Field(default=None)


class XRFAnalysis(SQLModel, table=True):
    """X‑Ray Fluorescence analysis."""
    __tablename__ = "xrf_analysis"

    xrf_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    notes: Optional[str] = Field(default=None)


class FermentationProfile(SQLModel, table=True):
    """Fermentation profile results."""
    __tablename__ = "fermentation_profile"

    fp_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    organism_id: Optional[int] = Field(default=None,
                                       description="Reference to organisms.organism_id",
                                       foreign_key="organisms.organism_id")
    product_type_id: Optional[int] = Field(default=None,
                                           description="Reference to product_type.product_type_id",
                                           foreign_key="product_type.product_type_id")
    product_value: Optional[Decimal] = Field(default=None)
    product_unit_id: Optional[int] = Field(default=None,
                                           description="Reference to units.unit_id",
                                           foreign_key="units.unit_id")
    notes: Optional[str] = Field(default=None)


class Organism(SQLModel, table=True):
    """Organism used in a fermentation."""
    __tablename__ = "organisms"

    organism_id: Optional[int] = Field(default=None, primary_key=True)
    organism_name: Optional[str] = Field(default=None)
    organism_strain_id: Optional[int] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class GasificationProfile(SQLModel, table=True):
    """Gasification profile results."""
    __tablename__ = "gasification_profile"

    gasification_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",
                                        foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",
                                    foreign_key="units.unit_id")
    notes: Optional[str] = Field(default=None)
    product_type_id: Optional[int] = Field(default=None,
                                           description="Reference to product_type.product_type_id",
                                           foreign_key="product_type.product_type_id")
    product_value: Optional[Decimal] = Field(default=None)
    product_unit_id: Optional[int] = Field(default=None,
                                           description="Reference to units.unit_id",
                                           foreign_key="units.unit_id")


class AutoclaveProfile(SQLModel, table=True):
    """Autoclave experiment results."""
    __tablename__ = "autoclave_profile"

    autoclave_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    product_type_id: Optional[int] = Field(default=None,
                                           description="Reference to product_type.product_type_id",
                                           foreign_key="product_type.product_type_id")
    product_value: Optional[Decimal] = Field(default=None)
    product_unit_id: Optional[int] = Field(default=None,
                                           description="Reference to units.unit_id",
                                           foreign_key="units.unit_id")


class AnalysisReplicate(SQLModel, table=True):
    """Link between a result and its replicate UUID (used for G‑Sheet tracking)."""
    __tablename__ = "analysis_replicate_id"

    analysis_replicate_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: Optional[int] = Field(default=None,
                                     description="Reference to analysis_results.result_id",
                                     foreign_key="analysis_results.result_id")
    analysis_types_id: Optional[int] = Field(default=None,
                                             description="Reference to analysis_types.analysis_type_id",
                                             foreign_key="analysis_types.analysis_type_id")
    analysis_replicate_uuid: Optional[str] = Field(default=None)


class ProductType(SQLModel, table=True):
    """Product type produced in a process (e.g., Butyric, Biochar)."""
    __tablename__ = "product_type"

    product_type_id: Optional[int] = Field(default=None, primary_key=True)
    product: Optional[str] = Field(default=None,
                                   description="e.g., Butyric, Iso‑Butyric, Propionic, Hydrogen, Syngas, Biochar, Indigoidine, 3HP, etc")
