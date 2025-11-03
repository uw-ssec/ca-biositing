# ca-biositing

A geospatial bioeconomy project for biositing analysis in California. This
repository provides tools for ETL pipelines to process data from Google Sheets
into PostgreSQL databases, geospatial analysis using QGIS, and a REST API for
data access.

## Project Structure

This project uses a **PEP 420 namespace package** structure with three main
components:

- **`ca_biositing.datamodels`**: Shared SQLModel database models and database
  configuration
- **`ca_biositing.pipeline`**: ETL pipelines orchestrated with Prefect, deployed
  via Docker
- **`ca_biositing.webservice`**: FastAPI REST API for data access

### Directory Layout

```text
ca-biositing/
├── src/ca_biositing/           # Namespace package root
│   ├── datamodels/             # Database models (SQLModel)
│   ├── pipeline/               # ETL pipelines (Prefect)
│   └── webservice/             # REST API (FastAPI)
├── resources/                  # Deployment resources
│   ├── docker/                 # Docker Compose configuration
│   └── prefect/                # Prefect deployment files
├── tests/                      # Integration tests
├── pixi.toml                   # Pixi dependencies and tasks
└── pixi.lock                   # Dependency lock file
```

## Quick Start

### Prerequisites

- **Pixi** (v0.55.0+):
  [Installation Guide](https://pixi.sh/latest/#installation)
- **Docker**: For running the ETL pipeline
- **Google Cloud credentials**: For Google Sheets access (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/uw-ssec/ca-biositing.git
cd ca-biositing

# Install dependencies with Pixi
pixi install

# Install pre-commit hooks
pixi run pre-commit-install
```

### Running Components

#### ETL Pipeline (Prefect + Docker)

**Note**: Before starting the services for the first time, create the required
environment file from the template:

```bash
cp resources/docker/.env.example resources/docker/.env
```

Then start and use the services:

```bash
# Start services (PostgreSQL, Prefect server, worker)
pixi run start-services

# Deploy flows to Prefect
pixi run deploy

# Run the ETL pipeline
pixi run run-etl

# Monitor via Prefect UI: http://localhost:4200

# Stop services
pixi run teardown-services
```

See [`resources/README.md`](resources/README.md) for detailed pipeline
documentation.

#### Web Service (FastAPI)

```bash
# Start the web service
pixi run start-webservice

# Access API docs: http://localhost:8000/docs
```

#### QGIS (Geospatial Analysis)

```bash
# Launch QGIS
pixi run qgis
```

**Note**: On macOS, you may see a Python faulthandler error - this is expected
and can be ignored. See
[QGIS Issue #52987](https://github.com/qgis/QGIS/issues/52987).

## Development

### Running Tests

```bash
# Run all tests
pixi run test

# Run tests with coverage
pixi run test-cov
```

### Code Quality

```bash
# Run pre-commit checks on staged files
pixi run pre-commit

# Run pre-commit on all files (before PR)
pixi run pre-commit-all
```

### Available Pixi Tasks

View all available tasks:

```bash
pixi task list
```

Key tasks:

- **Service Management**: `start-services`, `teardown-services`,
  `service-status`
- **ETL Operations**: `deploy`, `run-etl`
- **Development**: `test`, `test-cov`, `pre-commit`, `pre-commit-all`
- **Applications**: `start-webservice`, `qgis`
- **Database**: `access-db`, `check-db-health`

## Architecture

### Namespace Packages

This project uses **PEP 420 namespace packages** to organize code into
independently installable components that share a common namespace:

- Each component has its own `pyproject.toml` and can be installed separately
- Shared models in `datamodels` are used by both `pipeline` and `webservice`
- Clear separation of concerns while maintaining type consistency

### ETL Pipeline

The ETL pipeline uses:

- **Prefect**: Workflow orchestration and monitoring
- **Docker**: Containerized execution environment
- **PostgreSQL**: Data persistence
- **Google Sheets API**: Primary data source

Pipeline architecture:

1. **Extract**: Pull data from Google Sheets
2. **Transform**: Clean and normalize data with pandas
3. **Load**: Insert/update records in PostgreSQL via SQLModel

### Database Models

SQLModel-based models provide:

- Type-safe database operations
- Automatic schema generation (via Alembic)
- Shared models across ETL and API components
- Pydantic validation

## Project Components

### 1. Data Models (`ca_biositing.datamodels`)

Database models for:

- Biomass data (field samples, measurements)
- Geographic locations
- Experiments and analysis
- Metadata and samples
- Organizations and contacts

**Documentation**:
[`src/ca_biositing/datamodels/README.md`](src/ca_biositing/datamodels/README.md)

### 2. ETL Pipeline (`ca_biositing.pipeline`)

Prefect-orchestrated workflows for:

- Data extraction from Google Sheets
- Data transformation and validation
- Database loading and updates
- Lookup table management

**Documentation**:
[`src/ca_biositing/pipeline/README.md`](src/ca_biositing/pipeline/README.md)

**Guides**:

- [Docker Workflow](src/ca_biositing/pipeline/docs/DOCKER_WORKFLOW.md)
- [Prefect Workflow](src/ca_biositing/pipeline/docs/PREFECT_WORKFLOW.md)
- [ETL Development](src/ca_biositing/pipeline/docs/ETL_WORKFLOW.md)
- [Database Migrations](src/ca_biositing/pipeline/docs/ALEMBIC_WORKFLOW.md)

### 3. Web Service (`ca_biositing.webservice`)

FastAPI REST API providing:

- Read access to database records
- Interactive API documentation (Swagger/OpenAPI)
- Type-safe endpoints using Pydantic

**Documentation**:
[`src/ca_biositing/webservice/README.md`](src/ca_biositing/webservice/README.md)

### 4. Deployment Resources (`resources/`)

Docker and Prefect configuration for:

- Service orchestration (Docker Compose)
- Prefect deployments
- Database initialization

**Documentation**: [`resources/README.md`](resources/README.md)

## Adding Dependencies

### For Local Development (Pixi)

```bash
# Add conda package to default environment
pixi add <package-name>

# Add PyPI package to default environment
pixi add --pypi <package-name>

# Add to specific feature (e.g., pipeline)
pixi add --feature pipeline --pypi <package-name>
```

### For ETL Pipeline (Docker)

The pipeline dependencies are managed by Pixi's `etl` environment feature in
`pixi.toml`. When you add dependencies and rebuild Docker images, they are
automatically included:

```bash
# Add dependency to pipeline feature
pixi add --feature pipeline --pypi <package-name>

# Rebuild Docker images
pixi run rebuild-services

# Restart services
pixi run start-services
```

## Environment Management

This project uses **Pixi environments** for different workflows:

- **`default`**: General development, testing, pre-commit hooks
- **`gis`**: QGIS and geospatial analysis tools
- **`etl`**: ETL pipeline (used in Docker containers)
- **`webservice`**: FastAPI web service
- **`frontend`**: Node.js/npm for frontend development

## Frontend Integration

This repository includes the **Cal Bioscape Frontend** as a Git submodule in the
`frontend/` directory.

### Initializing the Submodule

```bash
# Initialize and pull the frontend submodule
pixi run submodule-frontend-init

# Install frontend dependencies
pixi run frontend-install

# Run frontend in development mode
pixi run frontend-dev

# Build production bundle
pixi run frontend-build
```

## Troubleshooting

### Services Won't Start

```bash
# Check service status
pixi run service-status

# View logs
pixi run service-logs

# Rebuild images
pixi run rebuild-services
```

## 📘 Documentation

This project uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for documentation.

### Local Preview

You can preview the documentation locally using [Pixi](https://pixi.sh/):

```bash
pixi install -e docs
pixi run -e docs docs-serve
```

Then open your browser and go to:
```
http://127.0.0.1:8000
```

### Database Issues

```bash
# Check database health
pixi run check-db-health

# Access database
pixi run access-db
```

### Pre-commit Failures

Pre-commit hooks may auto-fix files. If this happens:

1. Re-stage the fixed files: `git add <files>`
2. Re-run: `pixi run pre-commit`

## Documentation

### Component Documentation

- **Data Models**:
  [`src/ca_biositing/datamodels/README.md`](src/ca_biositing/datamodels/README.md)
- **ETL Pipeline**:
  [`src/ca_biositing/pipeline/README.md`](src/ca_biositing/pipeline/README.md)
- **Web Service**:
  [`src/ca_biositing/webservice/README.md`](src/ca_biositing/webservice/README.md)
- **Deployment Resources**: [`resources/README.md`](resources/README.md)

### Workflow Guides

- **Docker Workflow**:
  [`src/ca_biositing/pipeline/docs/DOCKER_WORKFLOW.md`](src/ca_biositing/pipeline/docs/DOCKER_WORKFLOW.md)
- **Prefect Workflow**:
  [`src/ca_biositing/pipeline/docs/PREFECT_WORKFLOW.md`](src/ca_biositing/pipeline/docs/PREFECT_WORKFLOW.md)
- **ETL Development**:
  [`src/ca_biositing/pipeline/docs/ETL_WORKFLOW.md`](src/ca_biositing/pipeline/docs/ETL_WORKFLOW.md)
- **Database Migrations**:
  [`src/ca_biositing/pipeline/docs/ALEMBIC_WORKFLOW.md`](src/ca_biositing/pipeline/docs/ALEMBIC_WORKFLOW.md)
- **Google Cloud Setup**:
  [`src/ca_biositing/pipeline/docs/GCP_SETUP.md`](src/ca_biositing/pipeline/docs/GCP_SETUP.md)

### AI Assistant Guidance

- **Main Repository**: [`AGENTS.md`](AGENTS.md)
- **Resources**: [`resources/AGENTS.md`](resources/AGENTS.md)
- **Data Models**:
  [`src/ca_biositing/datamodels/AGENTS.md`](src/ca_biositing/datamodels/AGENTS.md)
- **Pipeline**:
  [`src/ca_biositing/pipeline/AGENTS.md`](src/ca_biositing/pipeline/AGENTS.md)
- **Web Service**:
  [`src/ca_biositing/webservice/AGENTS.md`](src/ca_biositing/webservice/AGENTS.md)

## Project Resources

### Internal Resources

- 🔒 eScience Slack:
  [#ssec-ca-biositing](https://escience-institute.slack.com/archives/C098GJCTTFE)
- 🔒 SSEC Sharepoint:
  [Projects/GeospatialBioeconomy](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy?csf=1&web=1&e=VBUGQG)
- 🔒 Shared Folder:
  [SSEC CA Biositing](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy/SSEC%20CA%20Biositing%20Shared%20Folder?csf=1&web=1&e=p5wBel)

### Discussion & Support

- **General Discussion**:
  [GitHub Discussions](https://github.com/uw-ssec/ca-biositing/discussions)
- **Meeting Notes**:
  [discussions/meetings](https://github.com/uw-ssec/ca-biositing/discussions/categories/meetings)
- **Questions**: Contact [Anshul Tambay](https://github.com/atambay37)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidelines.

## License

See [`LICENSE`](LICENSE) for license information.

## Code of Conduct

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for our community guidelines.
