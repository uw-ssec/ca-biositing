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
│       └── main.py                  # FastAPI application
├── tests/                           # Test suite (to be added)
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

### Root Endpoint

- **GET** `/` - API information and version

### Hello Endpoint

- **GET** `/hello` - Simple hello world response

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
from sqlmodel import Session
from ca_biositing.datamodels.biomass import Biomass
from ca_biositing.datamodels.database import get_engine

engine = get_engine()

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/biomass")
def get_biomass(session: Session = Depends(get_session)):
    """Get all biomass entries."""
    biomass_items = session.query(Biomass).all()
    return biomass_items
```

## Package Information

- **Package Name**: `ca-biositing-webservice`
- **Version**: 0.1.0
- **Python**: >= 3.12
- **License**: BSD License
- **Repository**: <https://github.com/uw-ssec/ca-biositing>

## Contributing

See the main project's `CONTRIBUTING.md` for guidelines on contributing to this
package.
