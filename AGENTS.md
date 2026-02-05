# AGENTS.md

This file provides guidance to AI assistants when working with this repository.

## Repository Overview

This is the **ca-biositing** repository, a geospatial bioeconomy project for
biositing analysis in California. It provides tools for ETL (Extract, Transform,
Load) pipelines to process data from Google Sheets into PostgreSQL databases,
geospatial analysis using QGIS, a REST API for data access, and research
prototyping for bioeconomy site selection.

**Repository Stats:**

- **Type:** Research project / Data processing / Geospatial analysis
- **Architecture:** PEP 420 namespace packages
- **Build System:** Pixi (v0.55.0+) + Docker for ETL pipeline orchestration
- **Platform:** macOS (osx-arm64, osx-64), Linux (linux-64, linux-aarch64),
  Windows (win-64)
- **Languages:** Python (primary), SQL, TOML, Jupyter Notebooks
- **Domain:** Geospatial analysis, bioeconomy, ETL pipelines, database
  management

**Key Components:**

- **`ca_biositing.datamodels`**: SQLAlchemy database models. Uses LinkML as the
  source of truth.
- **`ca_biositing.pipeline`**: Prefect-orchestrated ETL workflows
  (Docker-based).
- **`ca_biositing.webservice`**: FastAPI REST API.
- **`resources/`**: Docker Compose and Prefect deployment configuration.
- **`frontend/`**: Git submodule for frontend application.

## Cross-Cutting Documentation

For detailed guidance on shared topics, see the `agent_docs/` directory:

| Topic              | Document                                                             | Description                        |
| ------------------ | -------------------------------------------------------------------- | ---------------------------------- |
| Namespace Packages | [agent_docs/namespace_packages.md](agent_docs/namespace_packages.md) | PEP 420 structure, import patterns |
| Testing Patterns   | [agent_docs/testing_patterns.md](agent_docs/testing_patterns.md)     | pytest fixtures, test commands     |
| Code Quality       | [agent_docs/code_quality.md](agent_docs/code_quality.md)             | Pre-commit, style, imports         |
| Troubleshooting    | [agent_docs/troubleshooting.md](agent_docs/troubleshooting.md)       | Common pitfalls and solutions      |
| Docker Workflow    | [agent_docs/docker_workflow.md](agent_docs/docker_workflow.md)       | Docker/Pixi service commands       |

## Build System & Environment Management

### Pixi Overview

This project uses **Pixi** for local development environment and dependency
management. Pixi handles both Conda and PyPI dependencies.

**ALWAYS use Pixi commands—never use conda, pip, or venv directly for local
development.**

**Note:** The ETL pipeline runs in Docker containers orchestrated by Pixi tasks.
Pixi is used for:

- Managing Docker services (start, stop, logs, status)
- Running code quality tools (pre-commit)
- Running tests (pytest)
- Running QGIS for geospatial analysis
- Deploying and running Prefect workflows
- Starting the FastAPI web service

### Environment Setup (ALWAYS RUN FIRST)

```bash
# Install the default environment (required before any other commands)
pixi install
```

**CRITICAL:** Always run `pixi install` before any other Pixi commands.

### Available Environments

1. **`default`**: Main development environment (datamodels, pipeline,
   webservice, gis).
2. **`gis`**: Geospatial analysis (QGIS, rasterio, xarray, shapely, pyproj).
3. **`etl`**: ETL pipeline environment (Prefect, SQLAlchemy, pandas).
4. **`webservice`**: Web service environment (FastAPI, uvicorn).
5. **`frontend`**: Frontend development (Node.js, npm).
6. **`docs`**: Documentation (MkDocs).
7. **`deployment`**: Cloud infrastructure (OpenTofu).

## Pathing & Namespace Packages

The repository uses PEP 420 namespace packages. The top-level namespace
`ca_biositing` is shared across three independent distributions:

- `src/ca_biositing/datamodels`
- `src/ca_biositing/pipeline`
- `src/ca_biositing/webservice`

All three are installed as editable PyPI packages into the Pixi environment via
`pixi.toml` feature dependencies. No `PYTHONPATH` manipulation is needed — after
`pixi install`, all packages are importable within any `pixi run` command.

### Jupyter Notebooks

This project uses [pixi-kernel](https://github.com/renan-r-santos/pixi-kernel)
for Jupyter integration. The kernel runs code inside the Pixi environment, so
all installed packages are available without any path configuration.

1. Run `pixi install` to set up the environment (includes `pixi-kernel`).
2. In VS Code or JupyterLab, select the **Pixi** kernel for your notebook.
3. All `ca_biositing` namespace packages are importable directly.

## Schema Management & Migrations (CRITICAL)

This project uses **LinkML** as the source of truth for the data model. The
schemas are maintained in the `resources/linkml/` directory, separate from the
installable Python package. Due to macOS Docker filesystem performance issues, a
specific local workflow is required.

### 1. LinkML Source of Truth

Modify YAML files in: `resources/linkml/modules/`

### 2. Orchestrated Update

Run the orchestration command to generate Python models, rebuild services, and
create a migration:

```bash
pixi run update-schema -m "Description of changes"
```

This task executes
[`orchestrate_schema_update.py`](resources/linkml/scripts/orchestrate_schema_update.py)
which:

- Generates SQLAlchemy models from LinkML.
- Rebuilds Docker services.
- **Generates the Alembic migration LOCALLY** to avoid container import hangs.

### 3. Apply Migrations

Apply changes to the database:

```bash
pixi run migrate
```

_Note: This runs `alembic upgrade head` locally against the Docker-hosted
PostgreSQL._

## Project Structure & Package Overviews

### `src/ca_biositing/datamodels`

The core data layer.

- `ca_biositing/datamodels/linkml/`: YAML schema definitions.
- `ca_biositing/datamodels/schemas/generated/`: Generated SQLAlchemy classes
  (**DO NOT EDIT**).
- `ca_biositing/datamodels/database.py`: Connection and session management.
- See
  [`src/ca_biositing/datamodels/README.md`](src/ca_biositing/datamodels/README.md).

### `src/ca_biositing/pipeline`

The ETL orchestration layer.

- `ca_biositing/pipeline/etl/`: Extract, Transform, and Load tasks.
- `ca_biositing/pipeline/flows/`: Prefect flow definitions.
- `ca_biositing/pipeline/utils/`: Helpers like `gsheet_to_pandas.py` and
  `lookup_utils.py`.
- See
  [`src/ca_biositing/pipeline/README.md`](src/ca_biositing/pipeline/README.md).

### `src/ca_biositing/webservice`

The API layer.

- `ca_biositing/webservice/main.py`: FastAPI application entrypoint.
- `ca_biositing/webservice/v1/endpoints/`: API route handlers.
- See
  [`src/ca_biositing/webservice/README.md`](src/ca_biositing/webservice/README.md).

## Validated Commands

### Docker Operations

- `pixi run start-services`: Start DB and Prefect.
- `pixi run service-status`: Check container health.
- `pixi run service-logs`: View logs.
- `pixi run rebuild-services`: Rebuild images after dependency changes.

### Development & Quality

- `pixi run pre-commit-all`: Run all checks (MANDATORY before PR).
- `pixi run test`: Run pytest suite.
- `pixi run start-webservice`: Launch API locally.

## Common Pitfalls

- **Import Errors**: Ensure you are running inside the Pixi environment
  (`pixi run ...`) or using the Pixi kernel in Jupyter.
- **macOS Geospatial Library Conflicts**: On macOS (especially Apple Silicon),
  you may encounter `PROJ` database version mismatch errors when using
  `geopandas` or `pyogrio`.
  - **Fix**: Ensure `PROJ_LIB` environment variable is set to the Pixi
    environment's data directory _before_ importing geospatial libraries.
  - **Example**:
    ```python
    import os, pyproj
    os.environ['PROJ_LIB'] = pyproj.datadir.get_data_dir()
    import geopandas as gpd
    ```
- **Docker Hangs & Deadlocks**:
  - **CRITICAL**: Never import heavy SQLAlchemy models or Pydantic settings at
    the module level. Always import them inside the `@task` or `@flow` function.
  - **CRITICAL**: Avoid any network I/O or database connectivity tests at the
    module level (import time).
  - **Docker Networking**: Inside containers, use the `db` hostname for
    PostgreSQL. Outside, use `localhost`.
- **GCP Auth**: `credentials.json` must be in the root for ETL tasks. See
  [`docs/pipeline/GCP_SETUP.md`](docs/pipeline/GCP_SETUP.md).

For more information on SSEC best practices, see:
<https://rse-guidelines.readthedocs.io/en/latest/llms-full.txt>
