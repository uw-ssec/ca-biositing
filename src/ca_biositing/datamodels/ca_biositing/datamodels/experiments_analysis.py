from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# Experiments & analyses
# ----------------------------------------------------------------------


class Experiment(SQLModel, table=True):
    """Experiment definition."""
    __tablename__ = "experiments"

    experiment_id: Optional[int] = Field(default=None, primary_key=True)
    exper_uuid: Optional[str] = Field(default=None, unique=True)
    gsheet_exper_id: Optional[int] = Field(default=None, unique=True,
                                            description="e.g., Ex05")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id",)
                                            # foreign_key="analysis_types.analysis_type_id")
    analysis_abbrev_id: Optional[int] = Field(default=None,
                                              description="Reference to analysis_abbreviations.analysis_abbreviations_id",)
                                              # foreign_key="analysis_abbreviations.analysis_abbreviations_id")
    exper_start_date: Optional[date] = Field(default=None)
    exper_duration: Optional[Decimal] = Field(default=None)
    exper_duration_unit_id: Optional[int] = Field(default=None,
                                                  description="Reference to units.unit_id",)
                                                  # foreign_key="units.unit_id")
    exper_location_id: Optional[int] = Field(default=None,
                                             description="Reference to geographic_locations.location_id",)
                                             # foreign_key="geographic_locations.location_id")
    exper_description: Optional[str] = Field(default=None)

    __table_args__ = (Index("idx_experiments_analysis_type_id", "analysis_type_id"),)


class ExperimentMethod(SQLModel, table=True):
    """Link table for many‑to‑many relationship between experiments and methods."""
    __tablename__ = "experiment_methods"

    experiment_method_id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: Optional[int] = Field(default=None,
                                         description="Reference to experiments.experiment_id",)
                                         # foreign_key="experiments.experiment_id")
    method_id: Optional[int] = Field(default=None,
                                      description="Reference to methods.method_id",)
                                      # foreign_key="methods.method_id")

    __table_args__ = (
        Index("idx_experiment_methods_method_id", "method_id"),
        Index("idx_experiment_methods_experiment_id", "experiment_id"),
    )


class AnalysisType(SQLModel, table=True):
    """Type of analysis (e.g., XRF, proximate)."""
    __tablename__ = "analysis_types"

    analysis_type_id: Optional[int] = Field(default=None, primary_key=True)
    analysis_name: Optional[str] = Field(default=None, unique=True,
                                          description="X‑Ray Fluorescence analysis, Proximate analysis, Chemical Composition, Fermentation Profile, etc.")


class AnalysisAbbreviation(SQLModel, table=True):
    """Abbreviation for an analysis type."""
    __tablename__ = "analysis_abbreviations"

    analysis_abbreviations_id: Optional[int] = Field(default=None, primary_key=True)
    analysis_abbreviation: Optional[str] = Field(default=None, unique=True,
                                                 description="XRF, Prox, Comp, etc.")


class AnalysisResult(SQLModel, table=True):
    """Result of a single analysis measurement."""
    __tablename__ = "analysis_results"

    result_id: Optional[int] = Field(default=None, primary_key=True)
    anlaysis_sample: Optional[int] = Field(default=None,
                                            description="Reference to preprocessed_samples.prepro_material_id",)
                                            # foreign_key="preprocessed_samples.prepro_material_id")
    experiment_id: Optional[int] = Field(default=None,
                                         description="Reference to experiments.experiment_id",)
                                         # foreign_key="experiments.experiment_id")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id",)
                                            # foreign_key="analysis_types.analysis_type_id")
    replicate_no: Optional[int] = Field(default=None)
    analysis_timestamp: Optional[datetime] = Field(default=None)
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id",)
                                        # foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                    description="Reference to units.unit_id",)
                                    # foreign_key="units.unit_id")
    qc_result_id: Optional[int] = Field(default=None,
                                         description="Reference to qc_results.qc_result_id",)
                                         # foreign_key="qc_results.qc_result_id")
    measurement_equipment_id: Optional[int] = Field(default=None,
                                                   description="Reference to equipment.equipment_id",)
                                                   # foreign_key="equipment.equipment_id")
    raw_data_url_id: Optional[int] = Field(default=None,
                                            description="Reference to url.url_id",)
                                            # foreign_key="url.url_id")
    analyst_id: Optional[int] = Field(default=None,
                                      description="Reference to analyst_contact.analyst_id",)
                                      # foreign_key="analyst_contact.analyst_id")
    analysis_note: Optional[str] = Field(default=None)

    __table_args__ = (
        Index("idx_analysis_results_parameter_id", "parameter_id"),
        Index("uq_analysis_results_experiment_parameter_replicate",
              "experiment_id", "parameter_id", "replicate_no", unique=True),
    )


class QCResult(SQLModel, table=True):
    """Quality‑control result (Pass/Fail)."""
    __tablename__ = "qc_results"

    qc_result_id: Optional[int] = Field(default=None, primary_key=True)
    qc_result: Optional[str] = Field(default=None, unique=True,
                                      description="Pass/Fail")


class Unit(SQLModel, table=True):
    """Unit of measurement."""
    __tablename__ = "units"

    unit_id: Optional[int] = Field(default=None, primary_key=True)
    unit: Optional[str] = Field(default=None, unique=True,
                                 description="% total weight, % dry weight, ppm, %")


class ParameterMethod(SQLModel, table=True):
    """Bridge table linking parameters to the methods that generate them."""
    __tablename__ = "parameter_methods"

    param_method_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_id: Optional[int] = Field(default=None,
                                         description="Reference to parameters.parameter_id",)
                                         # foreign_key="parameters.parameter_id")
    method_id: Optional[int] = Field(default=None,
                                      description="Reference to methods.method_id",)
                                      # foreign_key="methods.method_id")


class Method(SQLModel, table=True):
    """Analytical method definition."""
    __tablename__ = "methods"

    method_id: Optional[int] = Field(default=None, primary_key=True)
    method_name: Optional[str] = Field(default=None, unique=True)
    method_abbrev_id: Optional[int] = Field(default=None,
                                            description="Reference to method_abbrevs.method_abbrev_id",)
                                            # foreign_key="method_abbrevs.method_abbrev_id")
    method_category_id: Optional[int] = Field(default=None,
                                              description="Reference to method_categories.method_category_id",)
                                              # foreign_key="method_categories.method_category_id")
    method_standard_id: Optional[int] = Field(default=None,
                                              description="Reference to method_standards.method_standard_id",)
                                              # foreign_key="method_standards.method_standard_id")
    description: Optional[str] = Field(default=None)
    detection_limits: Optional[str] = Field(default=None)
    procedure_reference_id: Optional[int] = Field(default=None,
                                                  description="Reference to references.reference_id",)
                                                  # foreign_key="references.reference_id")
    method_url_id: Optional[int] = Field(default=None,
                                         description="Reference to url.url_id",)
                                         # foreign_key="url.url_id")

    __table_args__ = (Index("idx_methods_method_name", "method_name"),)


class MethodAbbreviation(SQLModel, table=True):
    """Abbreviation for a method (e.g., NREL, ASTM)."""
    __tablename__ = "method_abbrevs"

    method_abbrev_id: Optional[int] = Field(default=None, primary_key=True)
    method_abbrev: str = Field(..., unique=True,
                               description="NREL, ASTM")


class MethodCategory(SQLModel, table=True):
    """Category of a method (e.g., ICP, dry, wet)."""
    __tablename__ = "method_categories"

    method_category_id: Optional[int] = Field(default=None, primary_key=True)
    method_category: str = Field(..., unique=True,
                                 description="ICP method, CompAna method, dry, wet")


class MethodStandard(SQLModel, table=True):
    """Standard associated with a method (e.g., AOAC 997.02)."""
    __tablename__ = "method_standards"

    method_standard_id: Optional[int] = Field(default=None, primary_key=True)
    method_standard: str = Field(..., unique=True)


class Equipment(SQLModel, table=True):
    """Laboratory or field equipment."""
    __tablename__ = "equipment"

    equipment_id: Optional[int] = Field(default=None, primary_key=True)
    equipment_name: str = Field(..., unique=True,
                                description="Not null")
    equipment_room_id: Optional[int] = Field(default=None,
                                             description="Reference to rooms.room_id",)
                                             # foreign_key="rooms.room_id")
    description: Optional[str] = Field(default=None)


class MethodEquipment(SQLModel, table=True):
    """Many‑to‑many link between methods and equipment."""
    __tablename__ = "method_equipment"

    method_equipment_id: Optional[int] = Field(default=None, primary_key=True)
    method_id: Optional[int] = Field(default=None,
                                      description="Reference to methods.method_id",)
                                      # foreign_key="methods.method_id")
    equipment_id: Optional[int] = Field(default=None,
                                        description="Reference to equipment.equipment_id",)
                                        # foreign_key="equipment.equipment_id")

    __table_args__ = (
        Index("idx_method_equipment_method_id", "method_id"),
        Index("idx_method_equipment_equipment_id", "equipment_id"),
    )


class Parameter(SQLModel, table=True):
    """Parameter that can be measured or calculated."""
    __tablename__ = "parameters"

    parameter_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_name: Optional[str] = Field(default=None, unique=True)
    parameter_category_id: Optional[int] = Field(default=None,
                                                 description="Reference to parameter_catagories.parameter_catagory_id",)
                                                 # foreign_key="parameter_catagories.parameter_catagory_id")
    standard_unit_id: Optional[int] = Field(default=None,
                                            description="Reference to units.unit_id",)
                                            # foreign_key="units.unit_id")
    calculated: Optional[bool] = Field(default=None,
                                      description="If not calculated then it is measured directly. E.g. glucose vs glucan")
    description: Optional[str] = Field(default=None)
    typical_range_min: Optional[Decimal] = Field(default=None)
    typical_range_max: Optional[Decimal] = Field(default=None)


class ParameterCategory(SQLModel, table=True):
    """Category of a parameter (e.g., Fermentation, Minerals)."""
    __tablename__ = "parameter_catagories"

    parameter_catagory_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_catagory: Optional[str] = Field(default=None,
                                               description="Fermentation, Minerals, Elements, Compositional Analysis, etc")


class ParameterUnit(SQLModel, table=True):
    """Bridge table linking parameters to alternative units."""
    __tablename__ = "parameter_units"

    parameter_unit_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_id: Optional[int] = Field(default=None,
                                         description="Reference to parameters.parameter_id",)
                                         # foreign_key="parameters.parameter_id")
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id",)
                                   # foreign_key="units.unit_id")

    __table_args__ = (
        Index("idx_parameter_units_parameter_id", "parameter_id"),
        Index("idx_parameter_units_unit_id", "unit_id"),
    )


class ImportLog(SQLModel, table=True):
    """Log of data‑import operations."""
    __tablename__ = "import_log"

    import_id: Optional[int] = Field(default=None, primary_key=True)
    import_timestamp: Optional[datetime] = Field(default=None)
    destination: Optional[str] = Field(default=None)
    source_file: Optional[str] = Field(default=None)
    source_type: Optional[str] = Field(default=None,
                                       description="CSV, Excel, PDF extraction")
    records_imported: Optional[int] = Field(default=None)
    import_status: Optional[str] = Field(default=None)
    error_log: Optional[str] = Field(default=None)
    import_user: Optional[str] = Field(default=None)
