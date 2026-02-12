#!/usr/bin/env python3
"""
Conversion script to transform LinkML-generated SQLAlchemy classes to SQLModel classes.
This is a temporary tool - will be deleted after conversion is complete.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ColumnInfo:
    """Information about a column."""
    name: str
    type_str: str
    is_primary_key: bool
    is_nullable: bool
    is_unique: bool
    is_autoincrement: bool
    foreign_key: str | None
    default: str | None


@dataclass
class ModelInfo:
    """Information about a model class."""
    name: str
    tablename: str
    docstring: str | None
    columns: List[ColumnInfo]
    base_class: str  # "BaseEntity", "LookupBase", or "Base"


# Domain organization based on LinkML categories
DOMAIN_MAPPING = {
    # Core
    "EtlRun": "core/etl_run.py",
    "LineageGroup": "core/lineage.py",
    "EntityLineage": "core/lineage.py",
    "Note": "core/note.py",

    # Experiment & Equipment
    "Experiment": "experiment_equipment/experiment.py",
    "Equipment": "experiment_equipment/equipment.py",
    "ExperimentAnalysis": "experiment_equipment/experiment_links.py",
    "ExperimentEquipment": "experiment_equipment/experiment_links.py",
    "ExperimentMethod": "experiment_equipment/experiment_links.py",
    "ExperimentPreparedSample": "experiment_equipment/experiment_links.py",

    # Data Sources & Metadata
    "DataSource": "data_sources_metadata/data_source.py",
    "DataSourceType": "data_sources_metadata/data_source.py",
    "SourceType": "data_sources_metadata/data_source.py",
    "Dataset": "data_sources_metadata/dataset.py",
    "FileObjectMetadata": "data_sources_metadata/file_object_metadata.py",

    # External Data
    "Polygon": "external_data/polygon.py",
    "LandiqRecord": "external_data/landiq_record.py",
    "PrimaryAgProduct": "external_data/primary_ag_product.py",
    "BillionTon2023Record": "external_data/billion_ton.py",
    "UsdaCensusRecord": "external_data/usda_census.py",
    "UsdaCommodity": "external_data/usda_census.py",
    "UsdaDomain": "external_data/usda_census.py",
    "UsdaStatisticCategory": "external_data/usda_census.py",
    "UsdaSurveyRecord": "external_data/usda_survey.py",
    "UsdaSurveyProgram": "external_data/usda_survey.py",
    "UsdaTermMap": "external_data/usda_survey.py",
    "UsdaMarketReport": "external_data/usda_survey.py",
    "UsdaMarketRecord": "external_data/usda_survey.py",
    "LandiqResourceMapping": "external_data/landiq_resource_mapping.py",
    "ResourceUsdaCommodityMap": "external_data/resource_usda_commodity_map.py",

    # Field Sampling
    "FieldSample": "field_sampling/field_sample.py",
    "FieldSampleCondition": "field_sampling/field_sample_condition.py",
    "CollectionMethod": "field_sampling/collection_method.py",
    "HarvestMethod": "field_sampling/harvest_method.py",
    "FieldStorageMethod": "field_sampling/field_storage_method.py",
    "SoilType": "field_sampling/soil.py",
    "LocationSoilType": "field_sampling/soil.py",

    # General Analysis
    "Observation": "general_analysis/observation.py",
    "AnalysisType": "general_analysis/analysis_type.py",
    "DimensionType": "general_analysis/dimension_type.py",
    "FacilityRecord": "general_analysis/facility_record.py",
    "PhysicalCharacteristic": "general_analysis/physical_characteristic.py",

    # Infrastructure (all go to their own files)
    "InfrastructureBiodieselPlants": "infrastructure/biodiesel_plants.py",
    "InfrastructureBiosolidsFacilities": "infrastructure/biosolids_facilities.py",
    "InfrastructureCafoManureLocations": "infrastructure/cafo_manure_locations.py",
    "InfrastructureCombustionPlants": "infrastructure/combustion_plants.py",
    "InfrastructureDistrictEnergySystems": "infrastructure/district_energy_systems.py",
    "InfrastructureEthanolBiorefineries": "infrastructure/ethanol_biorefineries.py",
    "InfrastructureFoodProcessingFacilities": "infrastructure/food_processing_facilities.py",
    "InfrastructureLandfills": "infrastructure/landfills.py",
    "InfrastructureLivestockAnaerobicDigesters": "infrastructure/livestock_anaerobic_digesters.py",
    "InfrastructureMswToEnergy": "infrastructure/msw_to_energy.py",
    "InfrastructureSafAndRenewableDiesel": "infrastructure/saf_and_renewable_diesel.py",
    "InfrastructureWastewaterTreatment": "infrastructure/wastewater_treatment.py",
    "InfrastructurePetroleumPipelines": "infrastructure/petroleum_pipelines.py",

    # Methods, Parameters, Units
    "Method": "methods_parameters_units/method.py",
    "MethodAbbrev": "methods_parameters_units/method.py",
    "MethodCategory": "methods_parameters_units/method.py",
    "MethodStandard": "methods_parameters_units/method.py",
    "Parameter": "methods_parameters_units/parameter.py",
    "ParameterCategory": "methods_parameters_units/parameter.py",
    "ParameterCategoryParameter": "methods_parameters_units/parameter.py",
    "ParameterUnit": "methods_parameters_units/parameter.py",
    "Unit": "methods_parameters_units/unit.py",

    # People
    "Contact": "people/contact.py",
    "Provider": "people/provider.py",

    # Places
    "Place": "places/place.py",
    "LocationAddress": "places/location_address.py",
    "LocationResolution": "places/location_address.py",

    # Resource Information
    "Resource": "resource_information/resource.py",
    "ResourceClass": "resource_information/resource.py",
    "ResourceSubclass": "resource_information/resource.py",
    "ResourceMorphology": "resource_information/resource.py",
    "ResourceAvailability": "resource_information/resource_availability.py",
    "AgTreatment": "resource_information/ag_treatment.py",
    "Strain": "resource_information/strain.py",

    # Sample Preparation
    "PreparedSample": "sample_preparation/prepared_sample.py",
    "PreparationMethod": "sample_preparation/preparation_method.py",
    "PreparationMethodAbbreviation": "sample_preparation/preparation_method.py",
    "ProcessingMethod": "sample_preparation/processing_method.py",

    # Aim1 Records
    "ProximateRecord": "aim1_records/proximate_record.py",
    "UltimateRecord": "aim1_records/ultimate_record.py",
    "CompositionalRecord": "aim1_records/compositional_record.py",
    "IcpRecord": "aim1_records/icp_record.py",
    "XrfRecord": "aim1_records/xrf_record.py",
    "XrdRecord": "aim1_records/xrd_record.py",
    "CalorimetryRecord": "aim1_records/calorimetry_record.py",
    "FtnirRecord": "aim1_records/ftnir_record.py",
    "RgbRecord": "aim1_records/rgb_record.py",

    # Aim2 Records
    "PretreatmentRecord": "aim2_records/pretreatment_record.py",
    "FermentationRecord": "aim2_records/fermentation_record.py",
    "GasificationRecord": "aim2_records/gasification_record.py",
    "AutoclaveRecord": "aim2_records/autoclave_record.py",
}


def parse_column(col_node) -> ColumnInfo:
    """Parse a SQLAlchemy Column definition to extract column info."""
    name = None
    type_str = "Optional[str]"
    is_primary_key = False
    is_nullable = True
    is_unique = False
    is_autoincrement = False
    foreign_key = None
    default = "None"

    # Column arguments
    for arg in col_node.args:
        if isinstance(arg, ast.Call):
            type_name = ast.unparse(arg.func)
            # Map SQLAlchemy types to Python types
            if type_name == "Integer":
                type_str = "Optional[int]"
            elif type_name == "Text":
                type_str = "Optional[str]"
            elif type_name == "Float":
                type_str = "Optional[float]"
            elif type_name == "Numeric":
                type_str = "Optional[Decimal]"
            elif type_name == "Boolean":
                type_str = "Optional[bool]"
            elif type_name == "DateTime":
                type_str = "Optional[datetime]"
            elif type_name == "Date":
                type_str = "Optional[date]"
            elif type_name == "ForeignKey":
                # Extract FK target
                if arg.args:
                    foreign_key = ast.literal_eval(arg.args[0])

    # Column keyword arguments
    for kw in col_node.keywords:
        if kw.arg == "primary_key" and ast.literal_eval(kw.value):
            is_primary_key = True
        elif kw.arg == "nullable":
            is_nullable = ast.literal_eval(kw.value)
        elif kw.arg == "unique" and ast.literal_eval(kw.value):
            is_unique = True
        elif kw.arg == "autoincrement" and ast.literal_eval(kw.value):
            is_autoincrement = True

    # Adjust type based on nullability
    if not is_nullable and not is_primary_key:
        type_str = type_str.replace("Optional[", "").replace("]", "")

    return ColumnInfo(
        name=name,
        type_str=type_str,
        is_primary_key=is_primary_key,
        is_nullable=is_nullable,
        is_unique=is_unique,
        is_autoincrement=is_autoincrement,
        foreign_key=foreign_key,
        default=default,
    )


def sqlalchemy_type_to_python(type_str: str) -> str:
    """Map SQLAlchemy type to Python type annotation."""
    type_map = {
        "Integer": "int",
        "Text": "str",
        "Float": "float",
        "Numeric": "Decimal",
        "Boolean": "bool",
        "DateTime": "datetime",
        "Date": "date",
    }
    return type_map.get(type_str, "str")


def extract_column_info_from_line(line: str) -> Tuple[str, ColumnInfo] | None:
    """Extract column information from a Column definition line."""
    # Pattern: name = Column(...)
    match = re.match(r'\s+(\w+)\s*=\s*Column\((.*)\)', line)
    if not match:
        return None

    col_name = match.group(1)
    col_args = match.group(2)

    # Basic parsing
    is_primary_key = "primary_key=True" in col_args
    is_nullable = "nullable=False" not in col_args
    is_unique = "unique=True" in col_args
    is_autoincrement = "autoincrement=True" in col_args

    # Extract type
    type_str = "Optional[str]"
    if "Integer()" in col_args:
        type_str = "Optional[int]"
    elif "Text()" in col_args:
        type_str = "Optional[str]"
    elif "Float()" in col_args:
        type_str = "Optional[float]"
    elif "Numeric()" in col_args:
        type_str = "Optional[Decimal]"
    elif "Boolean()" in col_args:
        type_str = "Optional[bool]"
    elif "DateTime()" in col_args:
        type_str = "Optional[datetime]"
    elif "Date()" in col_args:
        type_str = "Optional[date]"

    # Extract foreign key
    foreign_key = None
    fk_match = re.search(r"ForeignKey\('([^']+)'\)", col_args)
    if fk_match:
        foreign_key = fk_match.group(1)

    # Adjust for primary keys
    if is_primary_key:
        type_str = type_str.replace("Optional[", "").replace("]", "") if "Optional" in type_str else type_str
        type_str = f"Optional[{type_str.replace('Optional[', '').replace(']', '')}]"

    # Adjust for non-nullable, non-PK fields
    if not is_nullable and not is_primary_key:
        type_str = type_str.replace("Optional[", "").replace("]", "")

    col_info = ColumnInfo(
        name=col_name,
        type_str=type_str,
        is_primary_key=is_primary_key,
        is_nullable=is_nullable,
        is_unique=is_unique,
        is_autoincrement=is_autoincrement,
        foreign_key=foreign_key,
        default="None" if "Optional" in type_str else None,
    )

    return (col_name, col_info)


def generate_sqlmodel_field(col: ColumnInfo) -> str:
    """Generate a SQLModel Field definition from column info."""
    # Build Field arguments
    field_args = []

    if col.is_primary_key:
        field_args.append("primary_key=True")

    if col.foreign_key:
        field_args.append(f'foreign_key="{col.foreign_key}"')

    if col.is_unique and not col.is_primary_key:
        field_args.append("unique=True")

    if not col.is_nullable and not col.is_primary_key:
        field_args.append("nullable=False")

    # Default value
    if col.is_primary_key or "Optional" in col.type_str:
        field_args.insert(0, "default=None")

    field_str = f"Field({', '.join(field_args)})" if field_args else "Field(default=None)"

    return f"    {col.name}: {col.type_str} = {field_str}"


def parse_generated_file(file_path: Path) -> Dict[str, ModelInfo]:
    """Parse the generated SQLAlchemy file and extract model information."""
    models = {}

    with open(file_path) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for class definitions (Base, BaseEntity, LookupBase, Aim1RecordBase, Aim2RecordBase)
        if line.startswith("class ") and ("(Base)" in line or "(BaseEntity)" in line or
                                          "(LookupBase)" in line or "(Aim1RecordBase)" in line or
                                          "(Aim2RecordBase)" in line):
            # Extract class name
            match = re.match(r'class (\w+)\((Base|BaseEntity|LookupBase|Aim1RecordBase|Aim2RecordBase)\):', line)
            if not match:
                i += 1
                continue

            class_name = match.group(1)
            parent_class = match.group(2)

            # Skip BaseEntity, LookupBase, Aim1RecordBase, Aim2RecordBase (will be recreated as mixins)
            if class_name in ["BaseEntity", "LookupBase", "Aim1RecordBase", "Aim2RecordBase"]:
                i += 1
                continue

            # Skip LandiqRecordView (managed by pgschema)
            if class_name == "LandiqRecordView":
                i += 1
                continue

            # Extract docstring
            docstring = None
            i += 1
            if i < len(lines) and '"""' in lines[i]:
                docstring = lines[i].strip().strip('"""')
                i += 1

            # Extract tablename
            tablename = None
            while i < len(lines) and not line.startswith("class "):
                if "__tablename__" in lines[i]:
                    match = re.search(r"__tablename__\s*=\s*'([^']+)'", lines[i])
                    if match:
                        tablename = match.group(1)
                    i += 1
                    break
                i += 1

            # Extract columns
            columns = []
            while i < len(lines):
                line = lines[i]

                # Stop at __repr__ or next class
                if "def __repr__" in line or (line.startswith("class ") and i > 0):
                    break

                # Parse column
                col_info = extract_column_info_from_line(line)
                if col_info:
                    col_name, col_data = col_info
                    columns.append(col_data)

                i += 1

            # Determine base class based on parent class from generated file
            if parent_class == "BaseEntity":
                base_class = "BaseEntity"
            elif parent_class == "LookupBase":
                base_class = "LookupBase"
            elif parent_class == "Aim1RecordBase":
                base_class = "Aim1RecordBase"
            elif parent_class == "Aim2RecordBase":
                base_class = "Aim2RecordBase"
            else:
                # For classes extending Base directly, determine appropriate base
                base_class = "SQLModel"
                if tablename and not (tablename.startswith("infrastructure_") or
                                     tablename == "place" or
                                     tablename in ["experiment_analysis", "experiment_equipment",
                                                 "experiment_method", "experiment_prepared_sample"]):
                    # Check if it looks like a lookup table
                    col_names = [c.name for c in columns if c.name]
                    if all(name in col_names for name in ["id", "name"]) and "created_at" not in col_names:
                        base_class = "LookupBase"
                    elif "id" in col_names and "created_at" in col_names:
                        base_class = "BaseEntity"

            models[class_name] = ModelInfo(
                name=class_name,
                tablename=tablename or class_name.lower(),
                docstring=docstring,
                columns=columns,
                base_class=base_class,
            )

        i += 1

    return models


def generate_sqlmodel_class(model: ModelInfo) -> str:
    """Generate a SQLModel class definition from model info."""
    lines = []

    # Class definition
    if model.base_class in ["BaseEntity", "LookupBase", "Aim1RecordBase", "Aim2RecordBase"]:
        lines.append(f"class {model.name}({model.base_class}, table=True):")
    else:
        lines.append(f"class {model.name}(SQLModel, table=True):")

    # Docstring
    if model.docstring:
        lines.append(f'    """{model.docstring}"""')

    # Tablename
    lines.append(f'    __tablename__ = "{model.tablename}"')
    lines.append("")

    # Fields (skip those provided by base class)
    base_fields = {
        "BaseEntity": ["id", "created_at", "updated_at", "etl_run_id", "lineage_group_id"],
        "LookupBase": ["id", "name", "description", "uri"],
        "Aim1RecordBase": ["id", "created_at", "updated_at", "etl_run_id", "lineage_group_id",
                          "record_id", "dataset_id", "experiment_id", "resource_id",
                          "prepared_sample_id", "technical_replicate_no", "technical_replicate_total",
                          "method_id", "analyst_id", "raw_data_id", "qc_pass", "note"],
        "Aim2RecordBase": ["id", "created_at", "updated_at", "etl_run_id", "lineage_group_id",
                          "record_id", "dataset_id", "experiment_id", "resource_id",
                          "prepared_sample_id", "technical_replicate_no", "technical_replicate_total",
                          "method_id", "analyst_id", "raw_data_id", "qc_pass", "note"],
    }

    skip_fields = base_fields.get(model.base_class, [])

    for col in model.columns:
        if col.name and col.name not in skip_fields:
            lines.append(generate_sqlmodel_field(col))

    return "\n".join(lines)


def organize_models_by_domain(models: Dict[str, ModelInfo]) -> Dict[str, List[ModelInfo]]:
    """Organize models by their target domain file."""
    domain_models = {}

    for model_name, model_info in models.items():
        domain_path = DOMAIN_MAPPING.get(model_name, "misc/misc.py")
        if domain_path not in domain_models:
            domain_models[domain_path] = []
        domain_models[domain_path].append(model_info)

    return domain_models


def generate_imports(models: List[ModelInfo]) -> List[str]:
    """Generate the necessary imports for a model file."""
    imports = set()
    imports.add("from typing import Optional")
    imports.add("from sqlmodel import Field, SQLModel")

    # Check if we need datetime/date/Decimal
    for model in models:
        for col in model.columns:
            if "datetime" in col.type_str:
                imports.add("from datetime import datetime")
            if "date" in col.type_str and "datetime" not in col.type_str:
                imports.add("from datetime import date")
            if "Decimal" in col.type_str:
                imports.add("from decimal import Decimal")

    # Check if we need base classes
    base_classes_needed = set(m.base_class for m in models if m.base_class not in ["SQLModel"])
    if base_classes_needed:
        base_imports = ", ".join(sorted(base_classes_needed))
        imports.add(f"from ..base import {base_imports}")

    return sorted(imports)


def write_domain_file(domain_path: str, models: List[ModelInfo], output_dir: Path):
    """Write a domain model file."""
    output_file = output_dir / domain_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    # Imports
    imports = generate_imports(models)
    lines.extend(imports)
    lines.append("")
    lines.append("")

    # Models
    for model in models:
        lines.append(generate_sqlmodel_class(model))
        lines.append("")
        lines.append("")

    with open(output_file, "w") as f:
        f.write("\n".join(lines))

    print(f"✓ Created {domain_path} ({len(models)} models)")


def create_init_files(domain_models: Dict[str, List[ModelInfo]], output_dir: Path):
    """Create __init__.py files for each subdirectory."""
    # Collect all subdirectories
    subdirs = set()
    for domain_path in domain_models.keys():
        parts = Path(domain_path).parts
        if len(parts) > 1:
            subdirs.add(parts[0])

    # Create __init__.py for each subdirectory
    for subdir in sorted(subdirs):
        init_file = output_dir / subdir / "__init__.py"
        init_file.parent.mkdir(parents=True, exist_ok=True)

        # Find all models in this subdirectory
        models_in_subdir = []
        for domain_path, models in domain_models.items():
            if domain_path.startswith(f"{subdir}/"):
                models_in_subdir.extend(models)

        # Write imports
        lines = []
        for model in sorted(models_in_subdir, key=lambda m: m.name):
            # Get the domain path, defaulting to misc if not in mapping
            model_domain = DOMAIN_MAPPING.get(model.name, "misc/misc.py")
            module_name = model_domain.replace(f"{subdir}/", "").replace(".py", "")
            lines.append(f"from .{module_name} import {model.name}")

        with open(init_file, "w") as f:
            f.write("\n".join(lines) + "\n")

        print(f"✓ Created {subdir}/__init__.py")


def create_main_init(domain_models: Dict[str, List[ModelInfo]], output_dir: Path):
    """Create the main models/__init__.py file."""
    init_file = output_dir / "__init__.py"

    lines = []
    lines.append("# Re-export all models for convenient imports")
    lines.append("from .base import BaseEntity, LookupBase, Aim1RecordBase, Aim2RecordBase")
    lines.append("")

    # Group by subdirectory
    subdirs = set()
    for domain_path in domain_models.keys():
        parts = Path(domain_path).parts
        if len(parts) > 1:
            subdirs.add(parts[0])

    for subdir in sorted(subdirs):
        models_in_subdir = []
        for domain_path, models in domain_models.items():
            if domain_path.startswith(f"{subdir}/"):
                models_in_subdir.extend(models)

        lines.append(f"# {subdir.replace('_', ' ').title()}")
        model_names = ", ".join(sorted(m.name for m in models_in_subdir))
        lines.append(f"from .{subdir} import {model_names}")
        lines.append("")

    with open(init_file, "w") as f:
        f.write("\n".join(lines))

    print(f"✓ Created models/__init__.py")


def main():
    """Main conversion function."""
    # Paths
    project_root = Path(__file__).parent.parent
    generated_file = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/ca_biositing.py"
    output_dir = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/models"

    print("🔄 Converting LinkML-generated SQLAlchemy to SQLModel...")
    print(f"   Input: {generated_file}")
    print(f"   Output: {output_dir}")
    print()

    # Parse generated file
    print("📖 Parsing generated models...")
    models = parse_generated_file(generated_file)
    print(f"   Found {len(models)} models (excluding BaseEntity, LookupBase, LandiqRecordView)")
    print()

    # Organize by domain
    print("📁 Organizing models by domain...")
    domain_models = organize_models_by_domain(models)
    print(f"   Organized into {len(domain_models)} domain files")
    print()

    # Write domain files
    print("✍️  Writing domain files...")
    for domain_path, domain_model_list in sorted(domain_models.items()):
        write_domain_file(domain_path, domain_model_list, output_dir)
    print()

    # Create __init__.py files
    print("📦 Creating __init__.py files...")
    create_init_files(domain_models, output_dir)
    create_main_init(domain_models, output_dir)
    print()

    print("✅ Conversion complete!")
    print()
    print("⚠️  Manual review required for edge cases:")
    print("   - Polygon: Add __table_args__ with functional index")
    print("   - Place: Uses text PK (geoid), no BaseEntity")
    print("   - Infrastructure tables: Domain-specific PKs, no BaseEntity")
    print("   - Numeric columns: May need sa_column_kwargs for precision")


if __name__ == "__main__":
    main()
