# CA Biositing Web Service Tests

This directory contains tests for the `ca-biositing-webservice` namespace
package.

## Test Structure

```text
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Shared pytest fixtures
├── test_package.py          # Package-level tests
├── test_main.py             # API endpoint tests
└── README.md                # This file
```

## Running Tests

### Run all tests in this package

```bash
pixi run pytest src/ca_biositing/webservice -v
```

### Run with coverage

```bash
pixi run pytest src/ca_biositing/webservice --cov=ca_biositing.webservice --cov-report=html --cov-report=term-missing
```

### Run specific test file

```bash
pixi run pytest src/ca_biositing/webservice/tests/test_main.py -v
```

## Test Coverage

Current test coverage includes:

- **Package Tests** (`test_package.py`):
  - Package version validation
  - Package imports validation

- **API Tests** (`test_main.py`):
  - Root endpoint (`/`)
  - Hello endpoint (`/hello`)
  - OpenAPI documentation endpoints
  - API metadata validation
  - Invalid endpoint handling (404)

## Fixtures

### `client` (from `conftest.py`)

Provides a FastAPI TestClient for making HTTP requests to the API.

**Usage:**

```python
def test_endpoint(client):
    response = client.get("/some-endpoint")
    assert response.status_code == 200
```

## Adding New Tests

When adding new API endpoints, create corresponding tests:

1. Add endpoint to `ca_biositing/webservice/main.py`
2. Add test function to `test_main.py` or create a new test file
3. Use the `client` fixture to make requests
4. Validate response status codes and JSON data
5. Run tests to verify implementation

## Dependencies

Tests require:

- `pytest` (>=8.4.2)
- `pytest-cov` (>=7.0.0)
- `httpx` (for TestClient, via fastapi)

These are automatically installed when using Pixi.
