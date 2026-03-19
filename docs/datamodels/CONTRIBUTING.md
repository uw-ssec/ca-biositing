# Contributing to CA Biositing Data Models

See the main project's [`CONTRIBUTING.md`](../CONTRIBUTING.md) for general
contribution guidelines (branching, PRs, commit style).

This document covers everything specific to the `ca-biositing-datamodels`
package.

## Package Structure

```text
src/ca_biositing/datamodels/
├── ca_biositing/
│   └── datamodels/
│       ├── __init__.py              # Package initialization and version
│       ├── config.py                # Model configuration (Pydantic Settings)
│       ├── database.py              # SQLModel engine and session management
│       ├── views.py                 # Materialized view definitions (7 views)
│       ├── models/                  # Hand-written SQLModel classes
│       │   ├── __init__.py          # Central re-export of all 91 models
│       │   ├── base.py              # Base classes (BaseEntity, LookupBase, etc.)
│       │   ├── aim1_records/        # Aim 1 analytical records
│       │   ├── aim2_records/        # Aim 2 processing records
│       │   ├── core/                # ETL lineage and run tracking
│       │   ├── data_sources_metadata/ # Data source and dataset metadata
│       │   ├── experiment_equipment/  # Experiments and equipment
│       │   ├── external_data/       # LandIQ, USDA, Billion Ton records
│       │   ├── field_sampling/      # Field samples and collection methods
│       │   ├── general_analysis/    # Observations and analysis types
│       │   ├── infrastructure/      # Infrastructure facility records
│       │   ├── methods_parameters_units/ # Methods, parameters, units
│       │   ├── misc/                # Additional infrastructure models
│       │   ├── people/              # Contacts and providers
│       │   ├── places/              # Location and address models
│       │   ├── resource_information/ # Resources, availability, strains
│       │   └── sample_preparation/  # Prepared samples and methods
│       └── sql_schemas/             # Reference SQL files (for pgschema validation)
├── tests/
│   ├── conftest.py                  # Pytest fixtures and configuration
│   ├── test_biomass.py              # Tests for biomass models
│   ├── test_geographic_locations.py # Tests for location models
│   └── test_package.py              # Tests for package metadata
├── LICENSE
├── README.md
└── pyproject.toml
```

## Model Categories

The 91 models span 15 domain subdirectories:

**Core and Infrastructure**
- `base.py` — Base classes (`BaseEntity`, `LookupBase`, `Aim1RecordBase`, `Aim2RecordBase`)
- `core/` — ETL run tracking and lineage (`EtlRun`, `EntityLineage`, `LineageGroup`)
- `infrastructure/` — Infrastructure facility records (biodiesel plants, landfills, ethanol biorefineries)
- `misc/` — Additional infrastructure models (MSW digesters, SAF plants, wastewater treatment)
- `places/` — Location and address models (`Place`, `LocationAddress`, `LocationResolution`)
- `people/` — Contact and provider information (`Contact`, `Provider`)
- `data_sources_metadata/` — Data source tracking (`DataSource`, `Dataset`, `FileObjectMetadata`)

**Resources and Sampling**
- `resource_information/` — Core resource entities (`Resource`, `ResourceClass`, `ResourceSubclass`, `ResourceAvailability`, `Strain`)
- `field_sampling/` — Field sampling data (`FieldSample`, `HarvestMethod`, `CollectionMethod`, `SoilType`)
- `sample_preparation/` — Sample processing (`PreparedSample`, `PreparationMethod`, `ProcessingMethod`)

**Experiments and Analysis**
- `experiment_equipment/` — Experimental setup (`Experiment`, `Equipment`, `ExperimentAnalysis`)
- `methods_parameters_units/` — Methods, parameters, and units (`Method`, `Parameter`, `Unit`, `MethodCategory`)
- `general_analysis/` — Observations and analysis results (`Observation`, `AnalysisType`, `PhysicalCharacteristic`)
- `aim1_records/` — Aim 1 analytical records (proximate, ultimate, compositional, ICP, XRD, XRF)
- `aim2_records/` — Aim 2 processing records (autoclave, fermentation, gasification, pretreatment)

**External Data**
- `external_data/` — Integration with external datasets (LandIQ, USDA Census, USDA Survey, Billion Ton 2023, USDA Market)

## Development Setup

Install the package in editable mode from the project root using Pixi:

```bash
pixi install
```

Or standalone for just this package:

```bash
cd src/ca_biositing/datamodels
pip install -e .
```

## Adding New Models

1. **Create model** — Add a new SQLModel class in the appropriate subdirectory
   under `models/`, or create a new subdirectory if needed.
2. **Re-export** — Add the import to `models/__init__.py` so the model is
   available from `ca_biositing.datamodels.models`.
3. **Generate migration** — Run `pixi run migrate-autogenerate -m "Add new model"`.
4. **Review** — Check the generated migration in `alembic/versions/`.
5. **Apply** — Run `pixi run migrate` to update the database.

## Modifying Existing Models

1. Edit the SQLModel class in its domain subdirectory.
2. Run `pixi run migrate-autogenerate -m "Describe change"`.
3. Review the migration script for accuracy.
4. Run `pixi run migrate`.

## Schema Management

All schema changes are managed through **Alembic migrations** generated from
SQLModel class definitions.

### Materialized Views

Views are defined in `ca_biositing/datamodels/views.py` and managed via manual
Alembic migration scripts (not autogenerated). After loading new data, refresh
them:

```bash
pixi run refresh-views
```

Check view status:

```bash
pixi run schema-analytics-list
```

### Validation with pgschema (Optional)

```bash
# Diff public schema
pixi run schema-plan

# Diff analytics schema (materialized views)
pixi run schema-analytics-plan
```

## Testing

```bash
# Run all tests
pixi run pytest src/ca_biositing/datamodels -v

# Run a specific test file
pixi run pytest src/ca_biositing/datamodels/tests/test_biomass.py -v

# Run with coverage
pixi run pytest src/ca_biositing/datamodels --cov=ca_biositing.datamodels --cov-report=html
```

## Code Quality

Before committing, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/datamodels/**/*
```
