# Contributing to CA Biositing Web Service

See the main project's [`CONTRIBUTING.md`](../CONTRIBUTING.md) for general
contribution guidelines (branching, PRs, commit style).

This document covers everything specific to the `ca-biositing-webservice`
package.

## Package Structure

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
├── tests/
│   ├── conftest.py                  # Fixtures (auth, httpx client)
│   └── test_smoke.py               # 16 endpoint smoke tests
├── LICENSE
├── README.md
└── pyproject.toml
```

## Development Setup

Install all dependencies from the project root:

```bash
pixi install
```

Or standalone for just this package (also requires `ca-biositing-datamodels`):

```bash
cd src/ca_biositing/webservice
pip install -e .
```

Start the development server:

```bash
pixi run start-webservice
```

Interactive docs are available at `http://localhost:8000/docs`.

## API Reference

### Auth

- `POST /v1/auth/token` — Obtain a JWT access token

### Discovery Endpoints

Each data family exposes discovery endpoints returning distinct queryable values
(all return `{ "values": ["..."] }`):

| Family   | Endpoints                                                                   |
| -------- | --------------------------------------------------------------------------- |
| Analysis | `/v1/feedstocks/analysis/resources`, `/geoids`, `/parameters`               |
| Census   | `/v1/feedstocks/usda/census/crops`, `/resources`, `/geoids`, `/parameters`  |
| Survey   | `/v1/feedstocks/usda/survey/crops`, `/resources`, `/geoids`, `/parameters`  |

### Data Endpoints

All crop, resource, and parameter lookups are **case-insensitive**.

**USDA Census** (`/v1/feedstocks/usda/census/`)
- `GET /crops/{crop}/geoid/{geoid}/parameters` — All census parameters for crop + geoid
- `GET /crops/{crop}/geoid/{geoid}/parameters/{param}` — Single parameter
- `GET /resources/{resource}/geoid/{geoid}/parameters` — All parameters by resource
- `GET /resources/{resource}/geoid/{geoid}/parameters/{param}` — Single parameter by resource

**USDA Survey** (`/v1/feedstocks/usda/survey/`) — Same structure as Census.

**Analysis** (`/v1/feedstocks/analysis/`)
- `GET /resources/{resource}/geoid/{geoid}/parameters` — All analysis parameters
- `GET /resources/{resource}/geoid/{geoid}/parameters/{param}` — Single parameter

Collection endpoints return `200` with an empty `data` list when a valid
crop/resource + geoid has no observations. Single-value endpoints return `404`
when the specific parameter is not found.

## Adding New Endpoints

1. Define the route in the appropriate file under `v1/feedstocks/` (or create a
   new router file and register it in `v1/router.py`).
2. Add any new response schemas to `v1/feedstocks/schemas.py`.
3. Add business logic in `services/`.
4. Add smoke tests in `tests/test_smoke.py`.
5. Start the server and verify the endpoint appears at `/docs`.

## Testing

```bash
# Run all tests
pixi run pytest src/ca_biositing/webservice -v

# Run with coverage
pixi run pytest src/ca_biositing/webservice --cov=ca_biositing.webservice --cov-report=html
```

The test suite requires a running database. See the project root
[`CONTRIBUTING.md`](../CONTRIBUTING.md) for environment setup.

## Code Quality

Before committing, run pre-commit checks:

```bash
pixi run pre-commit run --files src/ca_biositing/webservice/**/*
```
