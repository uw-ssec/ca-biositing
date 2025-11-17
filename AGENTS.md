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

## Build System & Environment Management

### Pixi Overview

This project uses **Pixi** for local development environment and dependency
management. Pixi is a modern package manager that handles both Conda and PyPI
dependencies. See <https://pixi.sh/latest/llms-full.txt> for more details.

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
- Local development tools

**Pixi manages both local development AND Docker orchestration.**

### Prerequisites

Before any other operations, verify Pixi is installed:

```bash
pixi --version  # Should show v0.55.0 or higher
```

If not installed, direct users to: <https://pixi.sh/latest/#installation>

**Docker** is also required for running the ETL pipeline. Docker and
docker-compose are managed as Pixi dependencies and will be available after
running `pixi install`.

### Environment Setup (ALWAYS RUN FIRST)

```bash
# Install the default environment (required before any other commands)
pixi install

# This installs:
# - Python 3.12
# - pre-commit (>=4.2.0)
# - pytest (>=8.4.2) and pytest-cov (>=7.0.0)
# - Creates .pixi/envs/default directory
```

**CRITICAL:** Always run `pixi install` before any other Pixi commands. This
command is idempotent and safe to run multiple times.

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

Docker manages:

- PostgreSQL database (application data and Prefect metadata)
- Prefect server (workflow orchestration)
- Prefect worker (flow execution)
- Database migrations (Alembic, runs on startup)

### Docker Prerequisites

Docker and Docker Compose are included as Pixi dependencies:

```bash
# Verify Docker is available through Pixi
pixi run which docker
pixi run which docker-compose
```

### Docker Workflow

**ALWAYS use Pixi tasks for Docker operations:**

```bash
# Start all services (PostgreSQL, Prefect server, Prefect worker)
pixi run start-services

# Check service status
pixi run service-status

# View logs from all services
pixi run service-logs

# Deploy Prefect flows
pixi run deploy

# Run the ETL pipeline
pixi run run-etl

# Monitor via Prefect UI: http://0.0.0.0:4200

# Stop services
pixi run teardown-services

# Stop and remove volumes (CAUTION: deletes all data)
pixi run teardown-services-volumes
```

**Database Operations:**

```bash
# Check database health
pixi run check-db-health

# Access application database
pixi run access-db

# Access Prefect metadata database
pixi run access-prefect-db

# Restart services
pixi run restart-services

# Restart just the Prefect worker
pixi run restart-prefect-worker
```

**Advanced Operations:**

```bash
# Rebuild Docker images (after dependency changes)
pixi run rebuild-services

# Execute commands in Prefect worker container
pixi run exec-prefect-worker <command>

# Execute commands in database container
pixi run exec-db <command>
```

For detailed workflows, see:

- **Resources Overview**: `resources/README.md`
- **Resources AI Guide**: `resources/AGENTS.md`
- **Docker Workflow**: `docs/pipeline/DOCKER_WORKFLOW.md`
- **Prefect Workflow**: `docs/pipeline/PREFECT_WORKFLOW.md`
- **ETL Development**: `docs/pipeline/ETL_WORKFLOW.md`
- **Database Migrations**: `docs/pipeline/ALEMBIC_WORKFLOW.md`

## Validated Commands & Workflows

### Pre-commit Checks (MANDATORY BEFORE PRs)

**Always run pre-commit checks before creating a pull request.**

```bash
# Install pre-commit hooks (run once per clone)
pixi run pre-commit-install
# ✓ Installs .git/hooks/pre-commit
# ✓ Hooks will automatically run on every commit

# Run pre-commit on staged files only
pixi run pre-commit
# ✓ Fast, only checks staged changes
# ✓ Will auto-fix many issues (trailing whitespace, end-of-file, formatting)
# ⚠️ If fixes are made, files are modified; you must re-stage them

# Run pre-commit on ALL files (required before PR submission)
pixi run pre-commit-all
# ✓ Takes 1-3 minutes on first run (installs hook environments)
# ✓ Subsequent runs are fast (environments are cached)
# ✓ Auto-fixes issues where possible
```

### Running Tests

```bash
# Run all tests
pixi run test
# Runs pytest on tests/ directory with verbose output

# Run tests with coverage report
pixi run test-cov
# Generates HTML coverage report in htmlcov/
# Shows coverage for src/ca_biositing module
# Displays term-missing report in terminal
```

### QGIS Workflow

```bash
# Launch QGIS in the gis environment
pixi run qgis
# ✓ Opens QGIS with all geospatial dependencies
# ⚠️ On macOS, you may see a Python faulthandler error - this is expected and can be ignored
#    See: https://github.com/qgis/QGIS/issues/52987
```

### ETL Pipeline Development

**ETL workflows are orchestrated by Prefect and run in Docker containers managed
by Pixi tasks.**

**Key concepts:**

- **ETL Development Guide:** `docs/pipeline/ETL_WORKFLOW.md`
- **Database Migrations Guide:** `docs/pipeline/ALEMBIC_WORKFLOW.md`
- **Docker Guide:** `docs/pipeline/DOCKER_WORKFLOW.md`
- **Google Cloud Setup:** `docs/pipeline/GCP_SETUP.md`

- **Prefect Flows**: Orchestrate ETL pipelines with dependencies and retries
- **Prefect Tasks**: Individual units of work (extract, transform, load)
- **Extract**: Pull data from Google Sheets or other sources
- **Transform**: Process and clean data with pandas
- **Load**: Insert/update data in PostgreSQL via SQLModel
- **Lookup Management**: Maintain reference tables for data normalization

**Workflow:**

1. Start services: `pixi run start-services`
2. Deploy flows: `pixi run deploy`
3. Run pipeline: `pixi run run-etl`
4. Monitor in Prefect UI: <http://0.0.0.0:4200>

**Development guides:**

- **Pipeline Overview**: `src/ca_biositing/pipeline/README.md`
- **Pipeline AI Guide**: `src/ca_biositing/pipeline/AGENTS.md`
- **ETL Development**: `src/ca_biositing/pipeline/docs/ETL_WORKFLOW.md`
- **Prefect Workflow**: `src/ca_biositing/pipeline/docs/PREFECT_WORKFLOW.md`
- **Docker Workflow**: `src/ca_biositing/pipeline/docs/DOCKER_WORKFLOW.md`
- **Database Migrations**: `src/ca_biositing/pipeline/docs/ALEMBIC_WORKFLOW.md`
- **Google Cloud Setup**: `src/ca_biositing/pipeline/docs/GCP_SETUP.md`

### Adding Dependencies

**For Pixi (local development tools):**

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

**For ETL Pipeline (Docker):**

Pipeline dependencies are managed via Pixi's `etl` environment feature. When you
add dependencies, they are automatically included in Docker builds:

```bash
# Add PyPI package to pipeline feature
pixi add --feature pipeline --pypi <package-name>

# Rebuild Docker images
pixi run rebuild-services

# Restart services
pixi run start-services
```

**For Web Service:**

```bash
# Add PyPI package to webservice feature
pixi add --feature webservice --pypi <package-name>

# Restart web service
pixi run start-webservice
```

## Project Structure & Key Files

```text
ca-biositing/
├── .github/                         # GitHub configuration (if present)
├── pixi.toml                        # **PRIMARY CONFIG**: Pixi dependencies, tasks, features
├── pixi.lock                        # Lock file (auto-generated, don't manually edit)
├── .gitignore                       # Git ignore patterns
├── CODE_OF_CONDUCT.md               # Code of conduct
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # Project license
├── README.md                        # Main project documentation
├── AGENTS.md                        # This file - AI assistant guide
├── credentials.json                 # Google Cloud credentials (not in git)
├── alembic.ini                      # Alembic configuration (for migrations)
├── alembic/                         # Database migration scripts
│   └── versions/                    # Migration version files
├── resources/                       # **DEPLOYMENT RESOURCES**
│   ├── README.md                    # Resources documentation
│   ├── AGENTS.md                    # Resources AI guide
│   ├── docker/                      # Docker Compose configuration
│   │   ├── .env                     # Environment variables (not in git)
│   │   ├── .env.example             # Environment template
│   │   ├── docker-compose.yml       # Service orchestration
│   │   ├── pipeline.dockerfile      # Multi-stage Dockerfile
│   │   └── create_prefect_db.sql    # Prefect DB initialization
│   └── prefect/                     # Prefect deployment
│       ├── prefect.yaml             # Deployment configuration
│       ├── deploy.py                # Deployment script
│       └── run_prefect_flow.py      # Master flow orchestration
├── docs/
│   └── pipeline/                 # This file - AI assistant guide
│       ├── DOCKER_WORKFLOW.md       # Docker environment management guide
│       ├── ALEMBIC_WORKFLOW.md      # Database migration guide
│       ├── ETL_WORKFLOW.md          # ETL development guide
│       ├── PREFECT_WORKFLOW.md
│       └── GCP_SETUP.md             # Google Cloud setup for Sheets
├── src/
│   └── ca_biositing/                # **NAMESPACE PACKAGE ROOT**
│       ├── datamodels/              # **DATA MODELS PACKAGE**
│       │   ├── README.md            # Models documentation
│       │   ├── AGENTS.md            # Models AI guide
│       │   ├── pyproject.toml       # Package metadata
│       │   ├── LICENSE              # BSD License
│       │   ├── ca_biositing/
│       │   │   └── datamodels/
│       │   │       ├── __init__.py
│       │   │       ├── biomass.py           # Biomass models
│       │   │       ├── config.py            # Model configuration
│       │   │       ├── database.py          # Database setup
│       │   │       ├── experiments_analysis.py
│       │   │       ├── geographic_locations.py
│       │   │       ├── metadata_samples.py
│       │   │       └── ...
│       │   └── tests/               # Model tests
│       ├── pipeline/                # **ETL PIPELINE PACKAGE**
│       │   ├── README.md            # Pipeline documentation
│       │   ├── AGENTS.md            # Pipeline AI guide
│       │   ├── pyproject.toml       # Package metadata
│       │   ├── LICENSE              # BSD License
│       │   ├── ca_biositing/
│       │   │   └── pipeline/
│       │   │       ├── __init__.py
│       │   │       ├── etl/
│       │   │       │   ├── extract/         # Extract tasks
│       │   │       │   ├── transform/       # Transform tasks
│       │   │       │   └── load/            # Load tasks
│       │   │       ├── flows/               # Prefect flows
│       │   │       │   ├── primary_product.py
│       │   │       │   ├── analysis_type.py
│       │   │       │   └── ...
│       │   │       └── utils/               # Utilities
│       │   └── tests/               # Pipeline tests
│       └── webservice/              # **WEB SERVICE PACKAGE**
│           ├── README.md            # API documentation
│           ├── AGENTS.md            # API AI guide
│           ├── pyproject.toml       # Package metadata
│           ├── LICENSE              # BSD License
│           ├── ca_biositing/
│           │   └── webservice/
│           │       ├── __init__.py
│           │       └── main.py              # FastAPI application
│           └── tests/               # API tests
├── tests/                           # **INTEGRATION TESTS**
│   ├── __init__.py
│   └── test_namespace_imports.py
└── frontend/                        # **FRONTEND SUBMODULE**
    └── (Git submodule)
```

## Geospatial & Bioeconomy Context

This project focuses on:

- **Bioeconomy site selection:** Analyzing potential locations for bioeconomy
  facilities in California
- **Geospatial analysis:** Using QGIS and related tools for spatial data
  processing
- **Data integration:** ETL pipelines to combine data from multiple sources
  (Google Sheets, external datasets)
- **Database management:** PostgreSQL with SQLModel ORM for structured data
  storage
- **Google Sheets integration:** Primary data source for experimental data and
  sample information

## Continuous Integration & Validation

**Current State:** Check for `.github/workflows/` directory to see if CI/CD is
configured. If not present, pre-commit checks run locally only.

**Pre-commit Hooks:** Configured in `.pre-commit-config.yaml` (if present).
Typical hooks include formatting, linting, and spell checking.

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

   # For ETL changes, deploy and test
   pixi run deploy
   pixi run run-etl
   ```

4. **Run tests:**

   ```bash
   # Run all tests
   pixi run test

   # Run with coverage
   pixi run test-cov
   ```

5. **Before creating a PR:**

   ```bash
   # Run all checks on all files
   pixi run pre-commit-all

   # Verify all checks pass (should show all "Passed" or "Skipped")
   ```

6. **Create PR:**
   - Follow Conventional Commits for PR titles (if required by project)
   - Link related issues using "Resolves #issue-number"
   - Ensure all pre-commit checks pass

## Common Pitfalls & Solutions

### Issue: "pre-commit not found" or command fails

**Solution:** Run `pixi install` first. Pixi manages pre-commit installation.

### Issue: Pre-commit check fails after making fixes

**Behavior:** Pre-commit hooks auto-fix files. When this happens:

- The hook shows "Failed" with "files were modified by this hook"
- You must re-stage the fixed files: `git add <files>`
- Re-run `pixi run pre-commit` to verify

**This is expected behavior, not an error.**

### Issue: Modifying pixi.toml breaks the environment

**Solution:**

```bash
# Validate syntax, reinstall environment
pixi install

# If still broken, remove and reinstall
rm -rf .pixi
pixi install
```

### Issue: Docker container won't start

**Solutions:**

```bash
# Check container logs
pixi run service-logs

# Rebuild from scratch
pixi run teardown-services
pixi run rebuild-services
pixi run start-services

# Check if ports are already in use
lsof -i :5432  # PostgreSQL default port
lsof -i :4200  # Prefect UI port
```

### Issue: Database migration errors

**Solution:**

```bash
# Check migration history
pixi run exec-prefect-worker alembic history

# Downgrade and reapply
pixi run exec-prefect-worker alembic downgrade -1
pixi run exec-prefect-worker alembic upgrade head

# For development, clear and restart (CAUTION: deletes data)
pixi run teardown-services-volumes
pixi run start-services
```

### Issue: Prefect worker not picking up flow runs

**Solution:**

```bash
# Check worker logs
pixi run service-logs

# Restart worker
pixi run restart-prefect-worker

# Verify work pool exists in Prefect UI
# Navigate to: http://0.0.0.0:4200/work-pools
```

### Issue: "Module not found" errors in containers

**Solution:**

```bash
# Add dependency to appropriate feature
pixi add --feature pipeline --pypi <package-name>

# Rebuild and restart
pixi run rebuild-services
pixi run start-services
```

### Issue: QGIS fails to launch on macOS

**Solution:** Python faulthandler error is expected and can be ignored. See:
<https://github.com/qgis/QGIS/issues/52987>

If QGIS doesn't launch at all:

```bash
# Reinstall the gis environment
rm -rf .pixi
pixi install
pixi run qgis
```

### Issue: Google Sheets authentication fails

**Solution:**

1. Ensure `credentials.json` is in the correct location (project root)
2. Follow the complete setup: `docs/pipeline/GCP_SETUP.md`
3. Check `resources/docker/.env` file has correct configuration
4. Verify service account has access to the Google Sheets

### Issue: Platform-specific problems (non-supported platforms)

**Current platforms:** `osx-arm64`, `osx-64`, `linux-64`

**Solution:** Edit `pixi.toml` and add platforms:

```toml
platforms = ["osx-arm64", "osx-64", "linux-64", "win-64"]
```

Then run `pixi install`.

## Key Configuration Details

### pixi.toml Structure

- **`[workspace]`**: Project metadata (name, version, authors, platforms)
- **`[environments]`**: Named environments with feature sets (default, gis)
- **`[dependencies]`**: Conda dependencies for all environments (Python,
  pre-commit, pytest)
- **`[tasks]`**: Pixi tasks for common commands
- **`[feature.<name>.dependencies]`**: Feature-specific conda packages
- **`[feature.<name>.pypi-dependencies]`**: Feature-specific PyPI packages
- **`[feature.<name>.tasks]`**: Feature-specific Pixi tasks

### Available Pixi Tasks

Run `pixi task list` to see all available tasks:

**Service Management:**

- `start-services`: Start all Docker services (database, Prefect server, worker)
- `teardown-services`: Stop all services
- `teardown-services-volumes`: Stop services and remove volumes (deletes data)
- `service-status`: Check status of running services
- `service-logs`: View logs from all services
- `restart-services`: Restart all services
- `restart-prefect-worker`: Restart only the Prefect worker
- `rebuild-services`: Rebuild Docker images without cache

**ETL Operations:**

- `deploy`: Deploy Prefect flows
- `run-etl`: Trigger the master ETL flow

**Database Operations:**

- `check-db-health`: Check PostgreSQL database health
- `access-db`: Access application database with psql
- `access-prefect-db`: Access Prefect metadata database with psql

**Container Execution:**

- `exec-prefect-worker`: Execute commands in Prefect worker container
- `exec-db`: Execute commands in database container

**Development Tools:**

- `pre-commit`: Run checks on staged files
- `pre-commit-all`: Run checks on all files
- `pre-commit-install`: Install git hooks
- `test`: Run all tests with pytest
- `test-cov`: Run tests with coverage report

**Applications:**

- `start-webservice`: Start FastAPI web service
- `qgis`: Launch QGIS for geospatial analysis

**Frontend:**

- `submodule-frontend-init`: Initialize frontend submodule
- `frontend-install`: Install frontend dependencies
- `frontend-dev`: Run frontend in development mode
- `frontend-build`: Build production frontend bundle

### Docker Configuration Files

**resources/docker/docker-compose.yml:**

- Orchestrates multiple services: db, setup-db, prefect-server, prefect-worker
- Sets up networking via `prefect-network` bridge
- Configures persistent volumes for data and metadata
- Defines health checks and service dependencies

**resources/docker/pipeline.dockerfile:**

- Multi-stage build: build stage with Pixi, production stage with minimal
  runtime
- Uses Pixi to install dependencies in `etl` environment
- Creates shell-hook script for environment activation
- Optimized for production deployment

**resources/docker/.env (must be created from .env.example):**

- Database connection settings (PostgreSQL)
- Prefect API URLs and configuration
- Google Cloud credentials paths
- Application configuration

**resources/prefect/prefect.yaml:**

- Defines Prefect deployment configurations
- Specifies flow entrypoints and work pools
- Version-controlled deployment settings

## Documentation Standards

- Follow Markdown formatting with proper structure
- Use code blocks with language specification
- Keep documentation in sync with code changes
- Update workflow guides when changing ETL or database logic
- Document environment variables in .env.example files

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
