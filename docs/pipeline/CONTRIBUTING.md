# Contributing to CA Biositing Pipeline

See the main project's [`CONTRIBUTING.md`](../CONTRIBUTING.md) for general
contribution guidelines (branching, PRs, commit style).

This document covers everything specific to the `ca-biositing-pipeline` package.

## Package Structure

```text
src/ca_biositing/pipeline/
├── ca_biositing/
│   └── pipeline/
│       ├── __init__.py              # Package initialization and version
│       ├── etl/
│       │   ├── extract/             # Data extraction tasks
│       │   │   ├── basic_sample_info.py
│       │   │   └── experiments.py
│       │   ├── transform/           # Data transformation tasks
│       │   │   └── products/
│       │   │       └── primary_ag_product.py
│       │   ├── load/                # Data loading tasks
│       │   │   └── products/
│       │   │       └── primary_ag_product.py
│       │   └── templates/           # ETL module templates
│       ├── flows/                   # Prefect flow definitions
│       │   ├── analysis_type.py
│       │   └── primary_ag_product.py
│       └── utils/                   # Utility functions
│           ├── gsheet_to_pandas.py
│           └── lookup_utils.py
├── tests/
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_etl_extract.py          # Tests for extract tasks
│   ├── test_flows.py                # Tests for Prefect flows
│   ├── test_lookup_utils.py         # Tests for utility functions
│   └── test_package.py              # Package metadata tests
├── LICENSE
├── README.md
├── pyproject.toml
├── alembic.ini
└── .env.example                     # Environment variables template
```

## Key Components

**Extract** (`etl/extract/`) — Pull data from Google Sheets or other sources.

**Transform** (`etl/transform/`) — Clean and reshape data with pandas.

**Load** (`etl/load/`) — Upsert transformed data into PostgreSQL.

**Flows** (`flows/`) — Prefect flows that combine extract/transform/load steps.

**Utilities** (`utils/`)
- `lookup_utils.py` — Foreign key helpers (`replace_name_with_id_df`, `replace_id_with_name_df`)
- `gsheet_to_pandas.py` — Google Sheets to DataFrame conversion

## Development Setup

Install all dependencies from the project root:

```bash
pixi install
```

Or standalone for just this package (also requires `ca-biositing-datamodels`):

```bash
cd src/ca_biositing/pipeline
pip install -e .
```

Copy `.env.example` to `.env` and fill in the database connection settings.

## Workflow Guides

Detailed step-by-step guides live alongside this file:

- **[DOCKER_WORKFLOW.md](./DOCKER_WORKFLOW.md)** — Managing dev containers
- **[ETL_WORKFLOW.md](./ETL_WORKFLOW.md)** — Running and extending the ETL pipeline
- **[ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)** — Database schema migrations
- **[GCP_SETUP.md](./GCP_SETUP.md)** — Google Sheets API / service account setup
- **[PREFECT_WORKFLOW.md](./PREFECT_WORKFLOW.md)** — Prefect flow orchestration

## Adding New ETL Pipelines

1. **Extract** — Create extraction task in `etl/extract/`
2. **Transform** — Create transformation task in `etl/transform/`
3. **Load** — Create loading task in `etl/load/`
4. **Flow** — Create a Prefect flow in `flows/` combining the three tasks
5. **Tests** — Add tests in `tests/`

Use `etl/templates/` as a starting point.

> **Note:** Database models are managed in the separate `ca-biositing-datamodels`
> package. See [`docs/datamodels/CONTRIBUTING.md`](../datamodels/CONTRIBUTING.md)
> for adding new models.

## Getting Started (Docker Environment)

1. Follow [GCP_SETUP.md](./GCP_SETUP.md) to configure Google Sheets API access.
2. Create `.env` from `.env.example`.
3. Build and start services:
   ```bash
   pixi run rebuild-services
   pixi run start-services
   ```
4. Apply database migrations:
   ```bash
   pixi run migrate
   ```
5. Run the ETL pipeline:
   ```bash
   pixi run run-etl
   ```

See [DOCKER_WORKFLOW.md](./DOCKER_WORKFLOW.md) and [ETL_WORKFLOW.md](./ETL_WORKFLOW.md)
for detailed instructions.

## Testing

```bash
# Run all tests
pixi run pytest src/ca_biositing/pipeline -v

# Run a specific test file
pixi run pytest src/ca_biositing/pipeline/tests/test_lookup_utils.py -v

# Run with coverage
pixi run pytest src/ca_biositing/pipeline --cov=ca_biositing.pipeline --cov-report=html
```

## Code Quality

Before committing, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/pipeline/**/*
```
