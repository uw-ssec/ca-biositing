# CA Biositing Pipeline

This package contains the ETL (Extract, Transform, Load) pipeline and workflows
for the CA Biositing project. It is implemented as a PEP 420 namespace package
that depends on the shared `ca-biositing-datamodels` package.

The pipeline extracts data from Google Sheets (or other sources), transforms it
using pandas and Python, and loads it into a PostgreSQL database using Prefect
for workflow orchestration.

## Overview

The `ca_biositing.pipeline` package provides:

- **ETL Tasks**: Prefect tasks for extracting, transforming, and loading data
- **Prefect Flows**: Workflow orchestration for data pipelines
- **Utility Functions**: Helpers for data transformation and database operations
- **Database Integration**: Uses shared datamodels from
  `ca-biositing-datamodels`
- **Google Sheets Integration**: Extract data from Google Sheets

## Structure

```text
src/ca_biositing/pipeline/
├── ca_biositing/
│   └── pipeline/
│       ├── __init__.py              # Package initialization and version
│       ├── etl/
│       │   ├── extract/             # Data extraction tasks
│       │   │   ├── __init__.py
│       │   │   ├── basic_sample_info.py
│       │   │   └── experiments.py
│       │   ├── transform/           # Data transformation tasks
│       │   │   └── products/
│       │   │       └── primary_product.py
│       │   ├── load/                # Data loading tasks
│       │   │   ├── analysis/
│       │   │   └── products/
│       │   │       └── primary_product.py
│       │   └── templates/           # ETL module templates
│       ├── flows/                   # Prefect flow definitions
│       │   ├── analysis_type.py
│       │   └── primary_product.py
│       └── utils/                   # Utility functions
│           ├── __init__.py
│           ├── gsheet_to_pandas.py
│           ├── lookup_utils.py
│           └── run_pipeline.py
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_etl_extract.py          # Tests for extract tasks
│   ├── test_flows.py                # Tests for Prefect flows
│   ├── test_lookup_utils.py         # Tests for utility functions
│   ├── test_package.py              # Package metadata tests
│   └── README.md                    # Test documentation
├── docs/                            # Documentation
│   ├── ALEMBIC_WORKFLOW.md
│   ├── DOCKER_WORKFLOW.md
│   ├── ETL_WORKFLOW.md
│   ├── GCP_SETUP.md
│   └── PREFECT_WORKFLOW.md
├── LICENSE                          # BSD License
├── README.md                        # This file
├── pyproject.toml                   # Package metadata and dependencies
├── alembic.ini                      # Alembic configuration
├── .env.example                     # Environment variables template
└── .dockerignore                    # Docker ignore patterns
```

## Core Workflows

This package has several key development workflows. For detailed, step-by-step
instructions, please refer to the dedicated workflow guides in the `docs/`
directory:

### 1. Docker Environment Management

- **Purpose:** Managing the lifecycle of your development containers (app and
  database)
- **Details:** Starting, stopping, and rebuilding your environment
- **[See: docs/DOCKER_WORKFLOW.md](./DOCKER_WORKFLOW.md)**

### 2. Database Schema Migrations (Alembic)

- **Purpose:** Making and applying changes to the database schema
- **Details:** How to automatically generate and apply migration scripts based
  on SQLModel changes
- **Note:** Database models are now in the shared `ca-biositing-datamodels`
  package
- **[See: docs/ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)**

### 3. ETL Pipeline Development (Prefect)

- **Purpose:** Running the ETL pipeline and adding new data pipelines
- **Details:** Using Prefect's flow orchestration with extract, transform, and
  load tasks
- **[See: docs/ETL_WORKFLOW.md](./ETL_WORKFLOW.md)**
- **[See: docs/PREFECT_WORKFLOW.md](./PREFECT_WORKFLOW.md)**

### 4. Google Cloud Setup

- **Purpose:** Setting up Google Sheets API access
- **Details:** Creating service account and credentials for data extraction
- **[See: docs/GCP_SETUP.md](./GCP_SETUP.md)**

## Installation

This package is part of the CA Biositing namespace package structure and depends
on the shared `ca-biositing-datamodels` package.

### As part of the full project

The recommended way to install is using Pixi (which manages all dependencies):

```bash
# From the main project root
pixi install
```

### Standalone installation (development)

For development of just the pipeline package:

```bash
cd src/ca_biositing/pipeline
pip install -e .
```

**Note:** This package requires the `ca-biositing-datamodels` package to be
installed as well.

## Testing

The package includes a test suite covering ETL functions, Prefect flows, and
utility functions.

### Run all tests

```bash
pixi run pytest src/ca_biositing/pipeline -v
```

### Run specific test files

```bash
pixi run pytest src/ca_biositing/pipeline/tests/test_lookup_utils.py -v
```

### Run with coverage

```bash
pixi run pytest src/ca_biositing/pipeline --cov=ca_biositing.pipeline --cov-report=html
```

See `tests/README.md` for detailed information about the test suite.

## Usage

### Importing Pipeline Components

```python
from ca_biositing.pipeline.etl.extract.basic_sample_info import extract_basic_sample_info
from ca_biositing.pipeline.flows.primary_product import primary_product_flow
from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df

# Use in your code
# ...
```

### Running Prefect Flows

```python
from ca_biositing.pipeline.flows.primary_product import primary_product_flow

# Run the flow
primary_product_flow()
```

### Using Utility Functions

```python
import pandas as pd
from sqlmodel import Session
from ca_biositing.datamodels.biomass import BiomassType
from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df

# Example: Replace biomass type names with IDs
df = pd.DataFrame({
    "sample_name": ["Sample1", "Sample2"],
    "biomass_type": ["Crop by-product", "Wood residue"]
})

with Session(engine) as session:
    df_with_ids = replace_name_with_id_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        name_column_name="biomass_type",
        id_column_name="biomass_type_id"
    )
```

## Getting Started (Docker Environment)

For production-like development using Docker containers:

**1. Google Cloud Setup:**

- Set up Google Sheets API access
- **[See: docs/GCP_SETUP.md](./GCP_SETUP.md)**

**2. Environment Setup:**

- Create a `.env` file from `.env.example`
- Configure database connection settings

**3. Build and Start Services:**

```bash
docker-compose build
docker-compose up -d
```

**4. Apply Database Migrations:**

```bash
docker-compose exec app alembic upgrade head
```

**5. Run ETL Pipeline:**

```bash
docker-compose exec app python utils/run_pipeline.py
```

See `docs/DOCKER_WORKFLOW.md` and `docs/ETL_WORKFLOW.md` for detailed
instructions.

## Key Components

### ETL Tasks

**Extract:** Data extraction from Google Sheets or other sources

- `extract/basic_sample_info.py`: Extract basic sample information
- `extract/experiments.py`: Extract experiment data

**Transform:** Data cleaning and transformation using pandas

- `transform/products/primary_product.py`: Transform primary product data

**Load:** Load transformed data into PostgreSQL

- `load/products/primary_product.py`: Load primary products into database

### Prefect Flows

Orchestrated workflows that combine ETL tasks:

- `flows/primary_product.py`: Primary product ETL flow
- `flows/analysis_type.py`: Analysis type ETL flow

### Utility Functions

**`lookup_utils.py`**: Helper functions for foreign key relationships

- `replace_id_with_name_df()`: Replace ID columns with names
- `replace_name_with_id_df()`: Replace name columns with IDs (get or create)

**`gsheet_to_pandas.py`**: Google Sheets to pandas DataFrame conversion

**`run_pipeline.py`**: Master script to run all ETL flows

## Dependencies

Core dependencies (defined in `pyproject.toml`):

- **ca-biositing-datamodels** >= 0.1.0: Shared database models
- **pandas** >= 2.2.0: Data manipulation
- **Prefect**: Workflow orchestration
- **gspread** & **gspread-dataframe**: Google Sheets integration
- **pyjanitor**: Data cleaning utilities
- **google-auth-oauthlib**: Google authentication
- **python-dotenv** >= 1.0.1: Environment variable management

## Development

### Code Quality

Before committing changes, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/pipeline/**/*
```

### Adding New ETL Pipelines

1. **Extract:** Create extraction task in `etl/extract/`
2. **Transform:** Create transformation task in `etl/transform/`
3. **Load:** Create loading task in `etl/load/`
4. **Flow:** Create Prefect flow in `flows/` that combines the tasks
5. **Tests:** Add tests in `tests/`
6. **Run:** Execute the flow

See `etl/templates/` for template files and `docs/ETL_WORKFLOW.md` for detailed
instructions.

### Adding Database Models

Database models are managed in the separate `ca-biositing-datamodels` package.
See that package's documentation for adding new models.

### Templates

Template files are available in `etl/templates/` to help create new ETL modules
following the project conventions.

## Package Information

- **Package Name**: `ca-biositing-pipeline`
- **Version**: 0.1.0
- **Python**: >= 3.12
- **License**: BSD License
- **Repository**: <https://github.com/uw-ssec/ca-biositing>

## Contributing

See the main project's `CONTRIBUTING.md` for guidelines on contributing to this
package.
