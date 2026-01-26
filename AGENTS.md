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
- **Size:** Medium (~100+ files including ETL modules, database models,
  workflows)
- **Languages:** Python (primary), SQL, TOML, Jupyter Notebooks
- **Build System:** Pixi (v0.55.0+) + Docker for ETL pipeline orchestration
- **Platform:** macOS (osx-arm64, osx-64), Linux (linux-64, linux-aarch64)
- **License:** See LICENSE file
- **Domain:** Geospatial analysis, bioeconomy, ETL pipelines, database
  management, workflow orchestration

**Key Components:**

- **`ca_biositing.datamodels`**: SQLModel database models (shared across
  components)
- **`ca_biositing.pipeline`**: Prefect-orchestrated ETL workflows (Docker-based)
- **`ca_biositing.webservice`**: FastAPI REST API
- **`resources/`**: Docker Compose and Prefect deployment configuration
- **`frontend/`**: Git submodule for frontend application

## Cross-Cutting Documentation

For detailed guidance on shared topics, see the `agent_docs/` directory:

| Topic | Document | Description |
|-------|----------|-------------|
| Namespace Packages | [agent_docs/namespace_packages.md](agent_docs/namespace_packages.md) | PEP 420 structure, import patterns |
| Testing Patterns | [agent_docs/testing_patterns.md](agent_docs/testing_patterns.md) | pytest fixtures, test commands |
| Code Quality | [agent_docs/code_quality.md](agent_docs/code_quality.md) | Pre-commit, style, imports |
| Troubleshooting | [agent_docs/troubleshooting.md](agent_docs/troubleshooting.md) | Common pitfalls and solutions |
| Docker Workflow | [agent_docs/docker_workflow.md](agent_docs/docker_workflow.md) | Docker/Pixi service commands |

## Build System & Environment Management

### Pixi Overview

This project uses **Pixi** for local development environment and dependency
management. Pixi is a modern package manager that handles both Conda and PyPI
dependencies. See <https://pixi.sh/latest/llms-full.txt> for more details.

**ALWAYS use Pixi commands—never use conda, pip, or venv directly for local
development.**

### Prerequisites

Before any other operations, verify Pixi is installed:

```bash
pixi --version  # Should show v0.55.0 or higher
```

If not installed, direct users to: <https://pixi.sh/latest/#installation>

### Environment Setup (ALWAYS RUN FIRST)

```bash
# Install the default environment (required before any other commands)
pixi install

# This installs Python 3.12, pre-commit, pytest, pytest-cov, docker-compose
# Creates .pixi/envs/default directory
```

**CRITICAL:** Always run `pixi install` before any other Pixi commands.

### Available Environments

1. **`default`** (main development environment)
   - Standard development environment
   - Core packages: Python 3.12, pre-commit, pytest, pytest-cov, docker-compose
   - Use for: general development, running pre-commit checks, running tests,
     Docker orchestration

2. **`gis`** (features: `qgis`, `raster`, `vector`)
   - Geospatial analysis environment
   - Includes: QGIS, rasterio, xarray, shapely, pyproj
   - Use for: geospatial analysis, QGIS workflows, working with raster/vector
     data

3. **`etl`** (features: `datamodels`, `pipeline`)
   - ETL pipeline environment (used in Docker containers)
   - Includes: Prefect, SQLModel, pandas, Google Sheets API clients
   - Use for: running ETL workflows in Docker

4. **`webservice`** (features: `datamodels`, `webservice`)
   - Web service environment
   - Includes: FastAPI, uvicorn, SQLModel
   - Use for: running the REST API

5. **`frontend`** (feature: `frontend`)
   - Frontend development environment
   - Includes: Node.js, npm
   - Use for: frontend development tasks

## Docker Environment (ETL Pipeline)

The ETL pipeline runs in Docker containers orchestrated by Prefect. Docker is
managed through **Pixi tasks** - never use docker-compose commands directly.

For detailed Docker commands, see [agent_docs/docker_workflow.md](agent_docs/docker_workflow.md).

### Quick Reference

```bash
# Start all services
pixi run start-services

# Check status and logs
pixi run service-status
pixi run service-logs

# Deploy and run ETL
pixi run deploy
pixi run run-etl

# Monitor via Prefect UI: http://0.0.0.0:4200

# Stop services
pixi run teardown-services
```

## Validated Commands & Workflows

### Pre-commit Checks (MANDATORY BEFORE PRs)

For detailed pre-commit workflow, see [agent_docs/code_quality.md](agent_docs/code_quality.md).

```bash
# Install hooks (run once per clone)
pixi run pre-commit-install

# Run on staged files
pixi run pre-commit

# Run on ALL files (required before PR)
pixi run pre-commit-all
```

### Running Tests

For detailed testing patterns, see [agent_docs/testing_patterns.md](agent_docs/testing_patterns.md).

```bash
# Run all tests
pixi run test

# Run tests with coverage
pixi run test-cov
```

### QGIS Workflow

```bash
# Launch QGIS in the gis environment
pixi run qgis
# On macOS, you may see a Python faulthandler error - this is expected
# See: https://github.com/qgis/QGIS/issues/52987
```

### Adding Dependencies

```bash
# Add a conda package to default environment
pixi add <package-name>

# Add a PyPI package to default environment
pixi add --pypi <package-name>

# Add to a specific feature (pipeline, webservice, etc.)
pixi add --feature <feature-name> <package-name>

# Always run after manual pixi.toml edits
pixi install
```

## Project Structure & Key Files

```text
ca-biositing/
├── .github/                         # GitHub configuration
├── pixi.toml                        # PRIMARY CONFIG: Pixi dependencies, tasks
├── pixi.lock                        # Lock file (auto-generated)
├── .gitignore                       # Git ignore patterns
├── CODE_OF_CONDUCT.md               # Code of conduct
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # Project license
├── README.md                        # Main project documentation
├── AGENTS.md                        # This file - AI assistant guide
├── agent_docs/                      # Cross-cutting AI documentation
│   ├── README.md                    # Index of agent docs
│   ├── namespace_packages.md        # PEP 420 structure
│   ├── testing_patterns.md          # Testing guidance
│   ├── code_quality.md              # Pre-commit, style
│   ├── troubleshooting.md           # Common pitfalls
│   └── docker_workflow.md           # Docker commands
├── credentials.json                 # Google Cloud credentials (not in git)
├── alembic.ini                      # Alembic configuration
├── alembic/                         # Database migration scripts
│   └── versions/                    # Migration version files
├── resources/                       # DEPLOYMENT RESOURCES
│   ├── README.md                    # Resources documentation
│   ├── AGENTS.md                    # Resources AI guide
│   ├── docker/                      # Docker Compose configuration
│   └── prefect/                     # Prefect deployment
├── docs/                            # Documentation
│   └── pipeline/                    # Pipeline workflow guides
├── src/
│   └── ca_biositing/                # NAMESPACE PACKAGE ROOT
│       ├── datamodels/              # DATA MODELS PACKAGE
│       │   ├── README.md
│       │   ├── AGENTS.md
│       │   ├── pyproject.toml
│       │   ├── ca_biositing/datamodels/
│       │   └── tests/
│       ├── pipeline/                # ETL PIPELINE PACKAGE
│       │   ├── README.md
│       │   ├── AGENTS.md
│       │   ├── pyproject.toml
│       │   ├── ca_biositing/pipeline/
│       │   └── tests/
│       └── webservice/              # WEB SERVICE PACKAGE
│           ├── README.md
│           ├── AGENTS.md
│           ├── pyproject.toml
│           ├── ca_biositing/webservice/
│           └── tests/
├── tests/                           # INTEGRATION TESTS
│   └── test_namespace_imports.py
└── frontend/                        # FRONTEND SUBMODULE
```

## Making Changes: Validated Workflow

1. **Setup (first time):**

   ```bash
   pixi install
   pixi run pre-commit-install
   ```

2. **Make your changes** to files

3. **Test changes:**

   ```bash
   # Stage your changes
   git add <files>

   # Run pre-commit checks
   pixi run pre-commit

   # If checks fail and auto-fix issues, re-add the fixed files
   git add <files>
   ```

4. **Run tests:**

   ```bash
   pixi run test
   ```

5. **Before creating a PR:**

   ```bash
   pixi run pre-commit-all
   ```

6. **Create PR:**
   - Follow Conventional Commits for PR titles (if required by project)
   - Link related issues using "Resolves #issue-number"
   - Ensure all pre-commit checks pass

## Key Configuration Details

### pixi.toml Structure

- **`[workspace]`**: Project metadata (name, version, authors, platforms)
- **`[environments]`**: Named environments with feature sets
- **`[dependencies]`**: Conda dependencies for all environments
- **`[tasks]`**: Pixi tasks for common commands
- **`[feature.<name>.dependencies]`**: Feature-specific conda packages
- **`[feature.<name>.pypi-dependencies]`**: Feature-specific PyPI packages

### Available Pixi Tasks

Run `pixi task list` to see all available tasks. Key tasks:

**Service Management:**
- `start-services`, `teardown-services`, `restart-services`
- `service-status`, `service-logs`
- `rebuild-services`

**ETL Operations:**
- `deploy`, `run-etl`

**Database:**
- `check-db-health`, `access-db`, `access-prefect-db`

**Development:**
- `pre-commit`, `pre-commit-all`, `pre-commit-install`
- `test`, `test-cov`

**Applications:**
- `start-webservice`, `qgis`

**Frontend:**
- `submodule-frontend-init`, `frontend-install`, `frontend-dev`, `frontend-build`

## Geospatial & Bioeconomy Context

This project focuses on:

- **Bioeconomy site selection:** Analyzing potential locations for bioeconomy
  facilities in California
- **Geospatial analysis:** Using QGIS and related tools for spatial data
  processing
- **Data integration:** ETL pipelines to combine data from multiple sources
- **Database management:** PostgreSQL with SQLModel ORM
- **Google Sheets integration:** Primary data source for experimental data

## Trust These Instructions

These instructions were generated through comprehensive analysis of the
repository structure and reference materials. Commands have been validated
against the project configuration. **Only perform additional searches if:**

- You need information not covered here
- Instructions appear outdated or produce errors
- You're implementing functionality that changes the build system or Docker
  setup

For routine tasks (adding files, making code changes, running checks), follow
these instructions directly without additional exploration.

For more information on SSEC best practices, see:
<https://rse-guidelines.readthedocs.io/en/latest/llms-full.txt>
