# CA Biositing Data Models

This package contains the SQLModel-based database models for the CA Biositing
project. It is implemented as a PEP 420 namespace package that can be shared
across multiple components of the application (ETL pipelines, API services,
etc.).

## Overview

The `ca_biositing.datamodels` package provides:

- **Database Models**: SQLModel classes representing database tables for
  biomass, geographic locations, experiments, samples, and more
- **Database Configuration**: Database connection and session management
  utilities
- **Model Configuration**: Shared configuration for model behavior using
  Pydantic Settings
- **Type Safety**: Full type annotations for all models and fields

## Structure

```text
src/ca_biositing/datamodels/
├── ca_biositing/
│   └── datamodels/
│       ├── __init__.py              # Package initialization and version
│       ├── biomass.py               # Biomass-related models (FieldSample, Biomass, etc.)
│       ├── config.py                # Model configuration
│       ├── database.py              # Database connection setup
│       ├── data_and_references.py   # Data and reference models
│       ├── experiments_analysis.py  # Experiment analysis models
│       ├── external_datasets.py     # External dataset models
│       ├── geographic_locations.py  # Geographic location models
│       ├── metadata_samples.py      # Sample metadata models
│       ├── organizations.py         # Organization models
│       ├── people_contacts.py       # People and contact models
│       ├── sample_preprocessing.py  # Sample preprocessing models
│       ├── specific_aalysis_results.py  # Analysis results models
│       ├── user.py                  # User models
│       └── templates/               # Model templates for new tables
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

```python
from ca_biositing.datamodels.biomass import (
    Biomass,
    FieldSample,
    BiomassType,
    PrimaryProduct
)
from ca_biositing.datamodels.geographic_locations import (
    GeographicLocation,
    City,
    State
)

# Create a model instance
sample = FieldSample(
    biomass_id=1,
    sample_name="Sample-001",
    amount_collected_kg=50.5
)
```

### Database Operations

```python
from sqlmodel import Session, create_engine
from ca_biositing.datamodels.biomass import Biomass

# Create engine and session
engine = create_engine("postgresql://user:pass@localhost/dbname")

# Use with SQLModel Session
with Session(engine) as session:
    # Query models
    biomass_items = session.query(Biomass).all()

    # Add new records
    new_biomass = Biomass(biomass_name="Corn Stover")
    session.add(new_biomass)
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

## Model Categories

### Biomass Models (`biomass.py`)

Core models for biomass entities, field samples, and related data:

- `Biomass`: Core biomass entity
- `FieldSample`: Sample metadata collected in the field
- `BiomassType`: Lookup table for biomass types
- `PrimaryProduct`: Lookup table for primary products
- `BiomassAvailability`: Seasonal and quantitative availability
- `BiomassQuality`: Qualitative attributes
- `BiomassPrice`: Pricing information
- `HarvestMethod`, `CollectionMethod`, `FieldStorage`: Lookup tables

### Geographic Models (`geographic_locations.py`)

Models for location data (can be anonymized):

- `GeographicLocation`: Main geographic location entity
- `StreetAddress`, `City`, `Zip`, `County`, `State`, `Region`: Location
  components
- `FIPS`: FIPS codes
- `LocationResolution`: Resolution types (GPS, county, etc.)

### Other Model Files

- `data_and_references.py`: Data sources and references
- `experiments_analysis.py`: Experimental analysis data
- `external_datasets.py`: External dataset integration
- `metadata_samples.py`: Sample metadata
- `organizations.py`: Organization information
- `people_contacts.py`: People and contact information
- `sample_preprocessing.py`: Sample preprocessing steps
- `specific_aalysis_results.py`: Analysis results
- `user.py`: User management

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

1. Create or modify model files in `ca_biositing/datamodels/`
2. Follow the existing patterns (use SQLModel, Field definitions, type hints)
3. Add corresponding tests in `tests/`
4. Generate Alembic migrations if needed (see main project documentation)
5. Run tests and pre-commit checks

### Model Templates

Template files are available in `ca_biositing/datamodels/templates/` to help
create new models following the project conventions.

## Package Information

- **Package Name**: `ca-biositing-datamodels`
- **Version**: 0.1.0
- **Python**: >= 3.12
- **License**: BSD License
- **Repository**: <https://github.com/uw-ssec/ca-biositing>

## Contributing

See the main project's `CONTRIBUTING.md` for guidelines on contributing to this
package.
