# ca-biositing

Discussion of general issues related to the project and protyping or research

## Relevant Links for project documentations and context

- eScience Slack channel: 🔒
  [#ssec-ca-biositing](https://escience-institute.slack.com/archives/C098GJCTTFE)
- SSEC Sharepoint (**INTERNAL SSEC ONLY**): 🔒
  [Projects/GeospatialBioeconomy](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy?csf=1&web=1&e=VBUGQG)
- Shared Sharepoint Directory: 🔒
  [SSEC CA Biositing Shared Folder](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy/SSEC%20CA%20Biositing%20Shared%20Folder?csf=1&web=1&e=p5wBel)

## General Discussions

For general discussion, ideas, and resources please use the
[GitHub Discussions](https://github.com/uw-ssec/ca-biositing/discussions).
However, if there's an internal discussion that need to happen, please use the
slack channel provided.

- Meeting Notes in GitHub:
  [discussions/meetings](https://github.com/uw-ssec/ca-biositing/discussions/categories/meetings)

## Questions

If you have any questions about our process, or locations of SSEC resources,
please ask [Anshul Tambay](https://github.com/atambay37).

## QGIS

This project includes QGIS for geospatial analysis and visualization. You can
run QGIS using pixi with the following command:

```bash
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

This repository now includes the **Cal Bioscape Frontend** as a Git submodule
located in the `frontend/` directory.

### Initializing the Submodule

When you first clone this repository, you can initialize and pull only the
`frontend` submodule with:

```bash
pixi run submodule-frontend-init
```

## 📘 Documentation

This project uses
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for
documentation.

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

### Contributing Documentation

Most documentation should live in the relevant directories within the `docs`
folder.

When adding new pages to the documentation, make sure you update the
[`mkdocs.yml` file](https://github.com/uw-ssec/ca-biositing/blob/main/mkdocs.yml)
so they can be rendered on the website.

If you need to add documentation referencing a file that lives elsewhere in the
repository, you'll need to do the following (this is an example, run from the
package root directory)

```bash
# symlink the file to its destination
# Be sure to use relative paths here, otherwise it won't work!
ln -s ../../deployment/README.md docs/deployment/README.md

# stage your new file
git add docs/deployment/README.md
```

Be sure to preview the documentation to make sure it's accurate before
submitting a PR.
