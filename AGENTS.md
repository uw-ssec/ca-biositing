# AGENTS.md

This file provides guidance to AI assistants when working with this repository.

## Repository Overview

This is the **ca-biositing** repository, a geospatial bioeconomy project for
biositing analysis in California. It provides tools for ETL (Extract, Transform,
Load) pipelines to process data from Google Sheets into PostgreSQL databases,
geospatial analysis using QGIS, and research prototyping for bioeconomy site
selection.

**Repository Stats:**

- **Type:** Research project / Data processing / Geospatial analysis
- **Size:** Medium (~50+ files including ETL modules, database models, and
  configuration)
- **Languages:** Python (primary), SQL, TOML, Jupyter Notebooks
- **Build System:** Pixi (v0.49.0+) + Docker for ETL pipeline
- **Platform:** macOS (osx-arm64, osx-64), Linux (linux-64)
- **License:** Not specified in main README
- **Domain:** Geospatial analysis, bioeconomy, ETL pipelines, database
  management

## Build System & Environment Management

### Pixi Overview

This project uses **Pixi** for local development environment and dependency
management. Pixi is a modern package manager that handles both Conda and PyPI
dependencies. See <https://pixi.sh/latest/llms-full.txt> for more details.

**ALWAYS use Pixi commands—never use conda, pip, or venv directly for local
development.**

**Note:** The ETL pipeline runs in Docker containers, not in the Pixi
environment. Pixi is used for:

- Running code quality tools (pre-commit)
- Running tests (pytest)
- Running QGIS for geospatial analysis
- Local development tools

### Prerequisites

Before any other operations, verify Pixi is installed:

```bash
pixi --version  # Should show v0.49.0 or higher
```

If not installed, direct users to: <https://pixi.sh/latest/#installation>

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
   - Core packages: Python 3.12, pre-commit, pytest, pytest-cov
   - Use for: general development, running pre-commit checks, running tests

2. **`gis`** (features: `qgis`, `raster`, `vector`)

   - Geospatial analysis environment
   - Includes: QGIS, rasterio, xarray, shapely, pyproj
   - Use for: geospatial analysis, QGIS workflows, working with raster/vector
     data

## Docker Environment (ETL Pipeline)

The ETL pipeline runs in Docker containers, separate from the Pixi environment.
Docker manages:

- PostgreSQL database
- ETL application container
- Alembic database migrations
- Production-like environment

### Docker Prerequisites

Ensure Docker and Docker Compose are installed:

```bash
docker --version
docker-compose --version
```

### Docker Workflow

**Initial Setup:**

```bash
# Navigate to the ETL project directory
cd etl_merge/my_etl_project

# Build the Docker image
docker-compose build

# Start services (database + app container)
docker-compose up -d

# Apply database migrations (first time only)
docker-compose exec app alembic upgrade head
```

**Common Docker Commands:**

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app

# Rebuild after dependency changes
docker-compose build --no-cache

# Run ETL pipeline
docker-compose exec app python run_pipeline.py

# Access PostgreSQL database
docker-compose exec db psql -U <username> -d <database>

# Run Alembic migrations
docker-compose exec app alembic upgrade head

# Generate new migration
docker-compose exec app python generate_migration.py
```

For detailed Docker workflows, see:
`etl_merge/my_etl_project/DOCKER_WORKFLOW.md`

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

**ETL workflows happen in Docker, not Pixi.** See the dedicated guides:

- **ETL Development Guide:** `etl_merge/my_etl_project/ETL_WORKFLOW.md`
- **Database Migrations Guide:** `etl_merge/my_etl_project/ALEMBIC_WORKFLOW.md`
- **Docker Guide:** `etl_merge/my_etl_project/DOCKER_WORKFLOW.md`
- **Google Cloud Setup:** `etl_merge/my_etl_project/GCP_SETUP.md`

**Key ETL concepts:**

- Extract modules: Pull data from Google Sheets or other sources
- Transform modules: Process and clean data
- Load modules: Insert data into PostgreSQL
- Templates available for new ETL modules in
  `etl_merge/my_etl_project/src/etl/templates/`

### Adding Dependencies

**For Pixi (local development tools):**

```bash
# Add a conda package to default environment
pixi add <package-name>

# Add a PyPI package to default environment
pixi add --pypi <package-name>

# Add to a specific feature (gis, etc.)
pixi add --feature <feature-name> <package-name>

# Always run after manual pixi.toml edits
pixi install
```

**For Docker (ETL application):**

1. Edit `etl_merge/my_etl_project/requirements.txt`
2. Rebuild Docker image: `docker-compose build`
3. Restart containers: `docker-compose up -d`

## Project Structure & Key Files

```text
.
├── .github/                         # GitHub configuration (if present)
├── pixi.toml                        # **PRIMARY CONFIG**: Pixi dependencies, tasks, features
├── pixi.lock                        # Lock file (auto-generated, don't manually edit)
├── .gitignore                       # Git ignore patterns
├── CODE_OF_CONDUCT.md               # Code of conduct
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # Project license
├── README.md                        # Main project documentation
├── AGENTS.md                        # This file - AI assistant guide
├── etl_merge/
│   └── my_etl_project/              # **ETL PIPELINE PROJECT (Docker-based)**
│       ├── README.md                # ETL project overview
│       ├── DOCKER_WORKFLOW.md       # Docker environment management guide
│       ├── ALEMBIC_WORKFLOW.md      # Database migration guide
│       ├── ETL_WORKFLOW.md          # ETL development guide
│       ├── GCP_SETUP.md             # Google Cloud setup for Sheets access
│       ├── docker-compose.yml       # Docker services definition
│       ├── Dockerfile               # Docker image build instructions
│       ├── requirements.txt         # Python dependencies for Docker
│       ├── alembic.ini              # Alembic configuration
│       ├── run_pipeline.py          # Main ETL pipeline script
│       ├── generate_migration.py    # Helper for generating migrations
│       ├── clear_alembic.py         # Helper for clearing migrations
│       ├── config.py                # Configuration management
│       ├── main.py                  # Application entry point
│       ├── .env                     # Environment variables (create from .env.example)
│       ├── alembic/                 # Database migration scripts
│       │   └── versions/            # Migration version files
│       ├── src/
│       │   ├── database.py          # Database connection setup
│       │   ├── etl/
│       │   │   ├── extract/         # Data extraction modules
│       │   │   ├── transform/       # Data transformation modules
│       │   │   ├── load/            # Data loading modules
│       │   │   └── templates/       # ETL module templates
│       │   ├── models/              # SQLModel database table definitions
│       │   │   └── templates/       # Database model templates
│       │   └── utils/               # Utility functions
│       └── tests/                   # ETL tests
├── src/
│   └── ca_biositing/                # Main Python package
│       ├── __init__.py
│       └── hello.py
└── tests/                           # Main project tests
    ├── __init__.py
    └── test_hello.py
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

   # For ETL changes, test in Docker
   cd etl_merge/my_etl_project
   docker-compose exec app python run_pipeline.py
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
docker-compose logs -f app

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check if ports are already in use
lsof -i :5432  # PostgreSQL default port
```

### Issue: Database migration errors

**Solution:**

```bash
# Check migration history
docker-compose exec app alembic history

# Downgrade and reapply
docker-compose exec app alembic downgrade -1
docker-compose exec app alembic upgrade head

# For development, clear and restart (CAUTION: deletes data)
docker-compose exec app python clear_alembic.py
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

1. Ensure `credentials.json` is in the correct location
2. Follow the complete setup: `etl_merge/my_etl_project/GCP_SETUP.md`
3. Check `.env` file has correct configuration
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

- `pre-commit`: Run checks on staged files
- `pre-commit-all`: Run checks on all files
- `pre-commit-install`: Install git hooks
- `test`: Run all tests with pytest
- `test-cov`: Run tests with coverage report
- `qgis`: Launch QGIS (requires gis environment)
- `run-qgis`: Internal task for QGIS execution

### Docker Configuration Files

**docker-compose.yml:**

- Defines services: app (ETL container) and db (PostgreSQL)
- Sets up networking and volumes
- Configures environment variables from .env

**Dockerfile:**

- Base image and Python setup
- Installs dependencies from requirements.txt
- Sets working directory and entry points

**.env file (must be created):**

- Database connection settings
- Google Cloud credentials paths
- Application configuration

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
