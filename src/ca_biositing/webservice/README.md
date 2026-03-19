# CA Biositing Web Service

This package contains the FastAPI REST API for the CA Biositing project. It is
implemented as a PEP 420 namespace package that depends on the shared
`ca-biositing-datamodels` package.

## Overview

The `ca_biositing.webservice` package provides:

- **REST API Endpoints**: FastAPI-based HTTP endpoints for data access
- **Data Integration**: Uses shared datamodels from `ca-biositing-datamodels`
- **Interactive Documentation**: Automatic Swagger/OpenAPI documentation
- **Type Safety**: Full type annotations using Pydantic and SQLModel

## Structure

```text
src/ca_biositing/webservice/
├── ca_biositing/
│   └── webservice/
│       ├── __init__.py              # Package initialization and version
│       ├── main.py                  # FastAPI application
│       ├── dependencies.py          # Dependency injection (DB session, auth)
│       ├── exceptions.py            # Custom HTTP exception classes
│       ├── services/                # Business logic layer
│       │   ├── analysis_service.py
│       │   ├── usda_census_service.py
│       │   ├── usda_survey_service.py
│       │   ├── _canonical_views.py  # Materialized view selectors
│       │   └── _usda_lookup_common.py  # Shared normalization helpers
│       └── v1/
│           ├── router.py            # API v1 router
│           ├── auth/
│           │   └── router.py        # JWT token endpoint
│           └── feedstocks/          # Protected data route definitions
│               ├── schemas.py       # Pydantic response models
│               ├── analysis.py
│               └── usda/
│                   ├── census.py
│                   └── survey.py
├── tests/                           # Integration smoke tests
│   ├── conftest.py                  # Fixtures (auth, httpx client)
│   └── test_smoke.py               # 16 endpoint smoke tests
├── LICENSE                          # BSD License
├── README.md                        # This file
└── pyproject.toml                   # Package metadata and dependencies
```

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

For development of just the web service package:

```bash
cd src/ca_biositing/webservice
pip install -e .
```

**Note:** This package requires the `ca-biositing-datamodels` package to be
installed as well.

## Usage

### Running the API Server

```bash
# From the main project root using Pixi
pixi run start-webservice

# Or using uvicorn directly
uvicorn ca_biositing.webservice.main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Importing API Components

```python
from ca_biositing.webservice.main import app

# Use in your code
# ...
```

## Available Endpoints

### Root & Auth

- **GET** `/` - API information and version
- **GET** `/v1/health` - Health check
- **POST** `/v1/auth/token` - Obtain JWT access token

### Discovery Endpoints

Each endpoint family exposes discovery endpoints that return the distinct
queryable values. All return `{ "values": ["..."] }`.

| Family   | Endpoints                                                                  |
| -------- | -------------------------------------------------------------------------- |
| Analysis | `/v1/feedstocks/analysis/resources`, `/geoids`, `/parameters`              |
| Census   | `/v1/feedstocks/usda/census/crops`, `/resources`, `/geoids`, `/parameters` |
| Survey   | `/v1/feedstocks/usda/survey/crops`, `/resources`, `/geoids`, `/parameters` |

### Data Endpoints

All crop, resource, and parameter lookups are **case-insensitive**.

**USDA Census** (`/v1/feedstocks/usda/census/`)

- **GET** `/crops/{crop}/geoid/{geoid}/parameters` - All census parameters for
  crop + geoid
- **GET** `/crops/{crop}/geoid/{geoid}/parameters/{param}` - Single parameter
- **GET** `/resources/{resource}/geoid/{geoid}/parameters` - All parameters by
  resource
- **GET** `/resources/{resource}/geoid/{geoid}/parameters/{param}` - Single
  parameter by resource

**USDA Survey** (`/v1/feedstocks/usda/survey/`) - Same structure as census.

**Analysis** (`/v1/feedstocks/analysis/`)

- **GET** `/resources/{resource}/geoid/{geoid}/parameters` - All analysis
  parameters
- **GET** `/resources/{resource}/geoid/{geoid}/parameters/{param}` - Single
  parameter

Collection endpoints (those ending in `/parameters`) return `200` with an empty
`data` list when a valid crop/resource + geoid combination has no observations.
Single-value endpoints return `404` when the specific parameter is not found.

## Dependencies

Core dependencies (defined in `pyproject.toml`):

- **ca-biositing-datamodels** >= 0.1.0: Shared database models
- **FastAPI** >= 0.115.0, < 1: Modern web framework
- **Uvicorn** >= 0.30.0, < 1: ASGI server

## Development

### Code Quality

Before committing changes, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/webservice/**/*
```

### Adding New Endpoints

1. **Define endpoint** in `ca_biositing/webservice/main.py`:

   ```python
   @app.get("/my-endpoint")
   def my_endpoint():
       """My endpoint description."""
       return {"data": "value"}
   ```

2. **Add tests** in `tests/` (when test suite is created)
3. **Run the server** and verify at `/docs`
4. **Test the endpoint** using the interactive documentation

### Using Database Models

```python
from fastapi import Depends
from sqlmodel import Session, select
from ca_biositing.datamodels.models import Resource
from ca_biositing.datamodels.database import get_engine, get_session

@app.get("/resources")
def get_resources(session: Session = Depends(get_session)):
    """Get all resource entries."""
    resources = session.exec(select(Resource)).all()
    return resources
```

## Package Information

- **Package Name**: `ca-biositing-webservice`
- **Version**: 0.1.0
- **Python**: >= 3.12
- **License**: BSD License
- **Repository**: <https://github.com/sustainability-software-lab/ca-biositing>

## Contributing

See the main project's `CONTRIBUTING.md` for guidelines on contributing to this
package.
