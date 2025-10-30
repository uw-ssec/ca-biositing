# CA Biositing Data Models

This package contains the SQLModel-based database models for the CA Biositing project.

## Overview

The `ca_biositing.datamodels` package provides:

- **Database Models**: SQLModel classes representing database tables
- **Database Configuration**: Database connection and session management
- **Model Configuration**: Shared configuration for model behavior

## Structure

```
datamodels/
├── __init__.py              # Package initialization and version
├── README.md                # This file
├── pyproject.toml           # Package metadata and dependencies
├── config.py                # Model configuration
├── database.py              # Database connection setup
├── biomass.py               # Biomass-related models
├── data_and_references.py   # Data and reference models
├── experiments_analysis.py  # Experiment analysis models
├── external_datasets.py     # External dataset models
├── geographic_locations.py  # Geographic location models
├── metadata_samples.py      # Sample metadata models
├── organizations.py         # Organization models
├── people_contacts.py       # People and contact models
├── sample_preprocessing.py  # Sample preprocessing models
├── specific_aalysis_results.py  # Analysis results models
├── user.py                  # User models
└── templates/               # Model templates
```

## Installation

This package is part of the CA Biositing namespace package structure. It can be installed
in editable mode:

```bash
pip install -e src/ca_biositing/datamodels
```

Or as part of the full project:

```bash
pixi install
```

## Usage

```python
from ca_biositing.datamodels.biomass import FieldSample
from ca_biositing.datamodels.database import get_session

# Use models in your application
with get_session() as session:
    samples = session.query(FieldSample).all()
```

## Dependencies

- SQLModel >= 0.0.19
- Alembic >= 1.13.2
- psycopg2 >= 2.9.9
- Pydantic Settings

## Development

See the main project documentation for development guidelines.
