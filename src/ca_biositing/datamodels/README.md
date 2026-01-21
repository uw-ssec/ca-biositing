# CA Biositing Data Models

This package contains the SQLModel-based database models for the CA Biositing
project. It is implemented as a PEP 420 namespace package that can be shared
across multiple components of the application (ETL pipelines, API services,
etc.).

## Overview

The `ca_biositing.datamodels` package provides:

- **LinkML Schema**: The single source of truth for the data model, defined in
  YAML.
- **Generated Database Models**: SQLModel classes automatically generated from
  the LinkML schema.
- **Database Configuration**: Database connection and session management
  utilities.
- **Model Configuration**: Shared configuration for model behavior using
  Pydantic Settings.
- **Type Safety**: Full type annotations for all models and fields.

## Schema Management Workflow

We use **LinkML** as the source of truth for our data schema. The workflow for
making schema changes is:

1.  **Modify LinkML Schema**: Edit the YAML files in
    `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/`.
2.  **Update Schema**: Run the orchestration command to generate Python models,
    rebuild services, and create a migration.
    ```bash
    pixi run update-schema -m "Description of changes"
    ```
    This command performs the following steps:
    - Cleans the generated models directory.
    - Generates new SQLAlchemy classes from the LinkML schema.
    - Generated schemas are IN A SINGLE .py FILE
      (datamodels/schemas/generate/ca_biositing)!
    - Rebuilds the Docker services to include the new code.
    - Starts the services.
    - Generates an Alembic migration script.
3.  **Apply Migration**: Apply the changes to the database.
    ```bash
    pixi run migrate
    ```

The generated Python models are saved in
`src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/`. **Do
not edit these files directly.** Always modify the LinkML schema and regenerate.

### Note on Unique Constraints

LinkML's SQLAlchemy generator does not always preserve `UNIQUE` constraints or
`identifier` status in a way that Alembic detects for all polymorphic tables.
The `generate_sqla.py` script includes a post-processing step to manually inject
`unique=True` for `record_id` on target classes (Observations and Aim Records)
to ensure robust upsert support.

## Structure

```text
src/ca_biositing/datamodels/
├── ca_biositing/
│   └── datamodels/
│       ├── __init__.py              # Package initialization and version
│       ├── config.py                # Model configuration
│       ├── database.py              # Database connection setup
│       ├── linkml/                  # LinkML schema source files
│       │   ├── ca_biositing.yaml    # Main schema entrypoint
│       │   └── modules/             # Modular schema definitions
│       ├── schemas/
│       │   └── generated/           # Generated SQLAlchemy classes (DO NOT EDIT)
│       └── utils/                   # Schema management scripts
│           ├── generate_sqla.py     # Script to generate models from LinkML
│           └── orchestrate_schema_update.py # Orchestration script
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures and configuration
│   ├── test_biomass.py              # Tests for biomass models
│   ├── test_geographic_locations.py # Tests for location models
│   ├── test_package.py              # Tests for package metadata
│   └── README.md                    # Test documentation
├── LICENSE                          # BSD License
├── README.md                        # This file
└── pyproject.toml                   # Package metadata and dependencies
```

## Installation

This package is part of the CA Biositing namespace package structure and is
designed to be shared across multiple components of the project.

### As part of the full project

The recommended way to install is using Pixi (which manages all dependencies):

```bash
pixi install
```

### Standalone installation (development)

For development of just the datamodels package:

```bash
cd src/ca_biositing/datamodels
pip install -e .
```

## Usage

### Importing Models

Models are generated into separate modules based on the LinkML schema structure.
You should import them from `ca_biositing.datamodels.schemas.generated`.

```python
from ca_biositing.datamodels.schemas.generated.resource_information import (
    Resource,
    ResourceClass,
    PrimaryCrop
)
from ca_biositing.datamodels.schemas.generated.field_sampling import FieldSample
from ca_biositing.datamodels.schemas.generated.places import (
    Geography,
    LocationAddress
)

# Create a model instance
sample = FieldSample(
    name="Sample-001",
    resource_id=1,
    amount_collected=50.5
)
```

### Database Operations

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from ca_biositing.datamodels.schemas.generated.ca_biositing import Resource

# Create engine and session
engine = create_engine("postgresql://user:pass@localhost/dbname")
Session = sessionmaker(bind=engine)

# Use with SQLAlchemy Session
with Session() as session:
    # Query models
    statement = select(Resource)
    resources = session.execute(statement).scalars().all()

    # Add new records
    new_resource = Resource(name="Corn Stover")
    session.add(new_resource)
    session.commit()
```

## Testing

The package includes a comprehensive test suite covering model instantiation,
field validation, and database persistence.

### Run all tests

```bash
pixi run pytest src/ca_biositing/datamodels -v
```

### Run specific test files

```bash
pixi run pytest src/ca_biositing/datamodels/tests/test_biomass.py -v
```

### Run with coverage

```bash
pixi run pytest src/ca_biositing/datamodels --cov=ca_biositing.datamodels --cov-report=html
```

See `tests/README.md` for detailed information about the test suite.

## Model Categories (LinkML Modules)

The schema is organized into modular YAML files in `linkml/modules/`. Each
module generates a corresponding Python file in `schemas/generated/`.

### Core & Infrastructure

- **`core.yaml`**: Base classes and shared types used across the schema.
- **`infrastructure.yaml`**: Infrastructure-related entities (e.g.,
  `InfrastructureType`, `Infrastructure`).
- **`places.yaml`**: Geographic location models (`GeographicLocation`, `City`,
  `State`, `County`, `Region`, `FIPS`).
- **`people.yaml`**: People and contact information (`Person`, `ContactInfo`,
  `Role`).
- **`data_sources_metadata.yaml`**: Metadata about data sources and references
  (`DataSource`, `Reference`).

### Biomass & Sampling

- **`resource_information.yaml`**: Core biomass entities (`Biomass`,
  `BiomassType`, `PrimaryProduct`, `BiomassAvailability`, `BiomassQuality`,
  `BiomassPrice`).
- **`field_sampling.yaml`**: Field sampling data (`FieldSample`,
  `HarvestMethod`, `CollectionMethod`, `FieldStorage`).
- **`sample_preparation.yaml`**: Sample preprocessing steps
  (`SamplePreprocessing`, `PreprocessingMethod`).
- **`lineage.yaml`**: Tracking sample lineage (`SampleLineage`).

### Experiments & Analysis

- **`experiment_equipment.yaml`**: Experimental setup and equipment
  (`Experiment`, `Equipment`).
- **`methods_parameters_units.yaml`**: Methods, parameters, and units (`Method`,
  `Parameter`, `Unit`).
- **`general_analysis.yaml`**: General analysis results (`AnalysisResult`,
  `AnalysisType`).
- **`aim1_records.yaml`**: Specific records for Aim 1 (`Aim1Record`).
- **`aim2_records.yaml`**: Specific records for Aim 2 (`Aim2Record`).

### External Data

- **`external_data.yaml`**: Integration with external datasets
  (`ExternalDataset`).

## Dependencies

Core dependencies (defined in `pyproject.toml`):

- **SQLModel** >= 0.0.19: SQL database interaction with Python type hints
- **Alembic** >= 1.13.2: Database migration tool
- **psycopg2** >= 2.9.9: PostgreSQL adapter for Python
- **Pydantic** >= 2.0.0: Data validation using Python type annotations
- **Pydantic Settings** >= 2.0.0: Settings management

## Development

### Code Quality

Before committing changes, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/datamodels/**/*
```

### Adding New Models

1.  **Modify LinkML**: Add the new class to the appropriate YAML file in
    `linkml/modules/`.
2.  **Update Schema**: Run `pixi run update-schema -m "Add new model"`.
3.  **Verify**: Check the generated file in `schemas/generated/` to ensure it
    looks correct.
4.  **Apply**: Run `pixi run migrate` to update the database.

## Package Information

- **Package Name**: `ca-biositing-datamodels`
- **Version**: 0.1.0
- **Python**: >= 3.12
- **License**: BSD License
- **Repository**: <https://github.com/uw-ssec/ca-biositing>

## Contributing

See the main project's `CONTRIBUTING.md` for guidelines on contributing to this
package.
