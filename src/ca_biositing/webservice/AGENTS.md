# AGENTS.md

This file provides guidance to AI assistants when working with the
ca-biositing-webservice namespace package.

## Package Overview

The **ca-biositing-webservice** package is a FastAPI-based REST API for the CA
Biositing project. It provides HTTP endpoints for accessing bioeconomy site
selection data and analysis results.

**Package Stats:**

- **Type:** REST API / Web Service
- **Size:** Small (~10-20 files expected)
- **Language:** Python 3.12+
- **Build System:** Hatchling (PEP 517)
- **Framework:** FastAPI (>=0.115.0, <1)
- **Server:** Uvicorn (>=0.30.0, <1)
- **Testing:** Pytest with TestClient
- **Namespace:** PEP 420 namespace package under `ca_biositing.webservice`

## Package Structure

```text
src/ca_biositing/webservice/
├── LICENSE                     # BSD License
├── README.md                   # Package documentation
├── pyproject.toml              # Package metadata and dependencies
├── AGENTS.md                   # This file
├── ca_biositing/
│   └── webservice/
│       ├── __init__.py         # Package initialization with version
│       └── main.py             # FastAPI application
└── tests/
    ├── __init__.py
    ├── conftest.py             # Shared pytest fixtures (TestClient)
    ├── test_package.py         # Package-level tests
    ├── test_main.py            # API endpoint tests
    └── README.md               # Test documentation
```

## FastAPI Application Pattern

### Main Application (`ca_biositing/webservice/main.py`)

```python
"""Main FastAPI application for CA Biositing API."""

from fastapi import FastAPI

# Import version from package
from . import __version__

# Create FastAPI app with metadata
app = FastAPI(
    title="CA Biositing API",
    description="REST API for CA Biositing bioeconomy site selection",
    version=__version__,
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to CA Biositing API",
        "version": __version__,
    }
```

**Key Patterns:**

- Always import `__version__` from package `__init__.py`
- Set app title, description, and version in FastAPI constructor
- Use async def for all endpoints (FastAPI best practice)
- Return dict objects (FastAPI automatically converts to JSON)
- Use type hints for request/response models

### Running the API

**Development server:**

```bash
# Navigate to web service directory
cd src/ca_biositing/webservice

# Run with uvicorn
uvicorn ca_biositing.webservice.main:app --reload

# Or with custom host/port
uvicorn ca_biositing.webservice.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access endpoints:**

- API: <http://localhost:8000>
- Interactive docs: <http://localhost:8000/docs>
- OpenAPI JSON: <http://localhost:8000/openapi.json>

## Testing Patterns

### TestClient Fixture (`tests/conftest.py`)

```python
"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from ca_biositing.webservice.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)
```

**Usage:**

```python
def test_endpoint(client):
    """Test an API endpoint."""
    response = client.get("/some-endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
```

### Endpoint Testing Pattern

```python
from fastapi import status

def test_read_item(client):
    """Test reading a single item."""
    # Make request
    response = client.get("/items/1")

    # Check status code
    assert response.status_code == status.HTTP_200_OK

    # Parse JSON response
    data = response.json()

    # Validate response structure
    assert "id" in data
    assert "name" in data
    assert data["id"] == 1
```

### Testing POST/PUT/DELETE Endpoints

```python
def test_create_item(client):
    """Test creating a new item."""
    # Prepare request body
    item_data = {
        "name": "Test Item",
        "description": "A test item",
    }

    # Make POST request
    response = client.post("/items", json=item_data)

    # Check status code
    assert response.status_code == status.HTTP_201_CREATED

    # Validate response
    data = response.json()
    assert data["name"] == item_data["name"]
    assert "id" in data
```

### Running Tests

```bash
# Run all web service tests
pixi run pytest src/ca_biositing/webservice -v

# Run with coverage
pixi run pytest src/ca_biositing/webservice --cov=ca_biositing.webservice --cov-report=html --cov-report=term-missing

# Run specific test file
pixi run pytest src/ca_biositing/webservice/tests/test_main.py -v

# Run specific test function
pixi run pytest src/ca_biositing/webservice/tests/test_main.py::test_read_root -v
```

## FastAPI Development Best Practices

### 1. Use Pydantic Models for Request/Response

```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    """Model for creating a new item."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class ItemResponse(BaseModel):
    """Model for item responses."""
    id: int
    name: str
    description: str | None

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item."""
    # Implementation
    pass
```

### 2. Use Path/Query Parameters

```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., gt=0),
    include_details: bool = Query(False),
):
    """Get item by ID with optional details."""
    pass
```

### 3. Use Dependency Injection

```python
from fastapi import Depends
from sqlmodel import Session
from ca_biositing.datamodels.database import get_session

@app.get("/biomass/{biomass_id}")
async def read_biomass(
    biomass_id: int,
    session: Session = Depends(get_session),
):
    """Get biomass record from database."""
    biomass = session.get(Biomass, biomass_id)
    if not biomass:
        raise HTTPException(status_code=404, detail="Biomass not found")
    return biomass
```

### 4. Use HTTP Exception for Errors

```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Get item by ID."""
    item = get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item
```

### 5. Use Router for Organization

```python
from fastapi import APIRouter

router = APIRouter(prefix="/biomass", tags=["biomass"])

@router.get("/")
async def list_biomass():
    """List all biomass records."""
    pass

@router.get("/{biomass_id}")
async def read_biomass(biomass_id: int):
    """Get specific biomass record."""
    pass

# In main.py
app.include_router(router)
```

## Integration with Datamodels

The API depends on `ca-biositing-datamodels` for database models:

```python
from ca_biositing.datamodels.biomass import Biomass, BiomassType
from ca_biositing.datamodels.database import get_session
from sqlmodel import Session, select
from fastapi import Depends

@app.get("/biomass", response_model=list[Biomass])
async def list_biomass(
    session: Session = Depends(get_session),
):
    """List all biomass records."""
    statement = select(Biomass)
    biomass_list = session.exec(statement).all()
    return biomass_list
```

## API Documentation

FastAPI automatically generates:

- **Interactive docs** (Swagger UI): `/docs`
- **Alternative docs** (ReDoc): `/redoc`
- **OpenAPI schema**: `/openapi.json`

**Customize documentation:**

```python
app = FastAPI(
    title="CA Biositing API",
    description="Comprehensive API description with Markdown formatting",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
```

## Common Tasks

### Adding a New Endpoint

1. **Define Pydantic models** (if needed):

   ```python
   class ItemCreate(BaseModel):
       name: str

   class ItemResponse(BaseModel):
       id: int
       name: str
   ```

2. **Add endpoint to `main.py`**:

   ```python
   @app.post("/items", response_model=ItemResponse, status_code=201)
   async def create_item(item: ItemCreate):
       # Implementation
       return {"id": 1, "name": item.name}
   ```

3. **Write tests in `tests/test_main.py`**:

   ```python
   def test_create_item(client):
       response = client.post("/items", json={"name": "Test"})
       assert response.status_code == 201
       data = response.json()
       assert data["name"] == "Test"
   ```

4. **Run tests**:

   ```bash
   pixi run pytest src/ca_biositing/webservice -v
   ```

### Adding Database Queries

1. **Import datamodels**:

   ```python
   from ca_biositing.datamodels.biomass import Biomass
   from ca_biositing.datamodels.database import get_session
   from sqlmodel import Session, select
   from fastapi import Depends
   ```

2. **Use dependency injection**:

   ```python
   @app.get("/biomass/{biomass_id}")
   async def read_biomass(
       biomass_id: int,
       session: Session = Depends(get_session),
   ):
       biomass = session.get(Biomass, biomass_id)
       if not biomass:
           raise HTTPException(status_code=404, detail="Not found")
       return biomass
   ```

3. **Test with mock database**:

   ```python
   @pytest.fixture
   def db_session():
       # Create in-memory database
       engine = create_engine("sqlite:///:memory:")
       SQLModel.metadata.create_all(engine)
       session = Session(engine)
       yield session
       session.close()

   def test_read_biomass(client, db_session):
       # Test implementation
       pass
   ```

### Adding Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    # Verify token logic
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return token

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    """Protected endpoint requiring authentication."""
    return {"message": "Access granted"}
```

## Dependencies

### Core Dependencies

- **fastapi** (>=0.115.0, <1): Web framework
- **uvicorn** (>=0.30.0, <1): ASGI server
- **httpx** (>=0.27.0): HTTP client for TestClient
- **ca-biositing-datamodels** (>=0.1.0): Database models

### Testing Dependencies

- **pytest** (>=8.4.2): Testing framework
- **pytest-cov** (>=7.0.0): Coverage reporting

## Common Pitfalls

### Issue: "ModuleNotFoundError: No module named 'ca_biositing.webservice'"

**Cause:** Package not installed or incorrect namespace structure

**Solution:**

```bash
# Install in development mode
pip install -e src/ca_biositing/webservice

# Verify structure (no __init__.py in ca_biositing/)
ls -la src/ca_biositing/
# Should show: webservice/ datamodels/ pipeline/ (no __init__.py)
```

### Issue: TestClient import fails

**Cause:** Missing httpx dependency

**Solution:** Add to `pyproject.toml`:

```toml
dependencies = [
    "httpx>=0.27.0",
]
```

### Issue: Database session errors in endpoints

**Cause:** Incorrect dependency injection or session management

**Solution:**

```python
# Correct pattern
from fastapi import Depends
from sqlmodel import Session
from ca_biositing.datamodels.database import get_session

@app.get("/items")
async def list_items(session: Session = Depends(get_session)):
    # Use session
    pass
```

### Issue: 422 Unprocessable Entity errors

**Cause:** Request body doesn't match Pydantic model

**Solution:**

- Check Pydantic model field types
- Use `Field()` for validation rules
- Test with correct JSON structure
- Check FastAPI `/docs` for expected schema

### Issue: CORS errors in browser

**Cause:** Missing CORS middleware

**Solution:**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development Workflow

1. **Start development server:**

   ```bash
   cd src/ca_biositing/webservice
   uvicorn ca_biositing.webservice.main:app --reload
   ```

2. **Make changes** to `main.py` or add new modules

3. **Test endpoints** in browser or with curl:

   ```bash
   curl http://localhost:8000/
   curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name":"Test"}'
   ```

4. **Write/update tests** in `tests/`

5. **Run tests:**

   ```bash
   pixi run pytest src/ca_biositing/webservice -v
   ```

6. **Check coverage:**

   ```bash
   pixi run pytest src/ca_biositing/webservice --cov=ca_biositing.webservice --cov-report=html
   open htmlcov/index.html
   ```

7. **Run pre-commit checks:**

   ```bash
   pixi run pre-commit-all
   ```

## API Design Guidelines

### RESTful URL Patterns

```text
GET    /items          # List all items
POST   /items          # Create new item
GET    /items/{id}     # Get specific item
PUT    /items/{id}     # Update item
DELETE /items/{id}     # Delete item
GET    /items/{id}/details  # Get item details (sub-resource)
```

### HTTP Status Codes

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request body
- **401 Unauthorized**: Missing/invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server error

### Response Format

```json
{
  "id": 1,
  "name": "Item Name",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**For errors:**

```json
{
  "detail": "Error description"
}
```

**For lists:**

```json
[
  { "id": 1, "name": "Item 1" },
  { "id": 2, "name": "Item 2" }
]
```

## Performance Considerations

### Use Async Properly

```python
# Good - async all the way
@app.get("/items")
async def list_items():
    return await get_items_async()

# Avoid - blocking in async
@app.get("/items")
async def list_items():
    return blocking_call()  # Blocks event loop

# If using blocking calls, use sync
@app.get("/items")
def list_items():
    return blocking_call()  # OK
```

### Database Connection Pooling

```python
# In database.py
engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=0,
)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_expensive_data(param: str):
    # Expensive operation
    return data

@app.get("/data/{param}")
async def read_data(param: str):
    return get_expensive_data(param)
```

## Documentation Standards

- Use docstrings for all endpoints
- Include parameter descriptions
- Document response models
- Add examples to Pydantic models
- Keep OpenAPI documentation up to date

## Trust These Instructions

These instructions were created specifically for the ca-biositing-webservice
namespace package following FastAPI best practices. Commands and patterns have
been validated against the project structure. **Only perform additional searches
if:**

- You need information about integrating with external services
- Instructions produce unexpected errors
- You're implementing advanced features (WebSockets, background tasks, etc.)

For routine API development (adding endpoints, testing, documentation), follow
these instructions directly.

For more information on SSEC best practices, see:
<https://rse-guidelines.readthedocs.io/en/latest/llms-full.txt>
