# AGENTS.md - CA Biositing Data Models

This file provides guidance to AI assistants when working with the
`ca-biositing-datamodels` namespace package.

## Package Overview

This is the **ca-biositing-datamodels** package, a PEP 420 namespace package
containing SQLModel-based database models for the CA Biositing project. It is
designed to be shared across multiple components (ETL pipelines, API services,
analysis tools) of the parent ca-biositing project.

**Package Stats:**

- **Type:** Python namespace package (PEP 420)
- **Package Name:** `ca-biositing-datamodels`
- **Import Name:** `ca_biositing.datamodels`
- **Version:** 0.1.0
- **Python:** >= 3.12
- **Build System:** Hatchling
- **License:** BSD License
- **Domain:** Database models, SQLModel, PostgreSQL, Data validation

## Key Concepts

### Namespace Package Structure

This package follows **PEP 420** implicit namespace package conventions:

```text
src/ca_biositing/datamodels/
├── ca_biositing/              # No __init__.py at this level (namespace)
│   └── datamodels/            # Package implementation
│       ├── __init__.py        # Package initialization
│       └── *.py               # Model modules
├── tests/                     # Test suite
├── pyproject.toml            # Package metadata
└── README.md                 # Documentation
```

**CRITICAL:** The `ca_biositing/` directory does **NOT** have an `__init__.py`
file. This allows multiple packages to share the `ca_biositing` namespace.

### Model Architecture

All models use **SQLModel**, which combines SQLAlchemy and Pydantic:

- Models are Python classes that represent database tables
- Use type hints for field definitions
- Include validation through Pydantic
- Support both ORM operations and API serialization

## Dependencies & Environment

### Core Dependencies

From `pyproject.toml`:

- **SQLModel** (>=0.0.19, <0.1): SQL database ORM with type hints
- **Alembic** (>=1.13.2, <2): Database migrations
- **psycopg2** (>=2.9.9, <3): PostgreSQL adapter
- **Pydantic** (>=2.0.0): Data validation
- **Pydantic Settings** (>=2.0.0): Configuration management

### Development Environment

This package is typically developed as part of the main ca-biositing project
using Pixi. See the main project's `AGENTS.md` for Pixi setup.

**For testing this package:**

```bash
# From the main project root
pixi run pytest src/ca_biositing/datamodels -v
```

**For standalone development:**

```bash
# From this directory
pip install -e .
pytest -v
```

## File Structure & Modules

### Model Modules

Located in `ca_biositing/datamodels/`:

1. **`biomass.py`** - Core biomass entities
   - `Biomass`: Main biomass entity
   - `FieldSample`: Field sample metadata
   - `BiomassType`, `PrimaryProduct`: Lookup tables
   - `BiomassAvailability`, `BiomassQuality`, `BiomassPrice`: Related data
   - `HarvestMethod`, `CollectionMethod`, `FieldStorage`: Lookup tables

2. **`geographic_locations.py`** - Location models
   - `GeographicLocation`: Main location entity (can be anonymized)
   - `StreetAddress`, `City`, `Zip`, `County`, `State`, `Region`: Components
   - `FIPS`: FIPS codes
   - `LocationResolution`: Resolution types

3. **`experiments_analysis.py`** - Experiment data
4. **`metadata_samples.py`** - Sample metadata
5. **`data_and_references.py`** - Data sources and references
6. **`external_datasets.py`** - External dataset integration
7. **`organizations.py`** - Organization information
8. **`people_contacts.py`** - People and contacts
9. **`sample_preprocessing.py`** - Preprocessing steps
10. **`specific_aalysis_results.py`** - Analysis results
11. **`user.py`** - User management

### Configuration & Utilities

- **`config.py`**: Model configuration using Pydantic Settings
- **`database.py`**: Database connection and session management
- **`__init__.py`**: Package metadata and version

### Templates

- **`templates/`**: Template files for creating new model modules

## Working with Models

### Model Definition Patterns

**Standard SQLModel Table:**

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class MyTable(SQLModel, table=True):
    """Description of the table."""
    __tablename__ = "my_table"

    # Primary key with auto-increment
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier"
    )

    # Required field
    name: str = Field(
        default=None,
        index=True,
        description="Name of the entity"
    )

    # Optional field
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes"
    )

    # Numeric field (use Decimal for precision)
    value: Optional[Decimal] = Field(
        default=None,
        description="Numeric value"
    )

    # Foreign key reference (commented for flexibility)
    parent_id: Optional[int] = Field(
        default=None,
        index=True,
        description="Reference to parent table"
        # foreign_key="parent_table.id"
    )

    # Timestamp with default
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )
```

### Important Conventions

1. **Type Hints:** Always use proper type hints (`str`, `int`, `Optional[T]`)
2. **Decimal for Currency/Precision:** Use `Decimal` for financial or
   high-precision numeric fields
3. **Optional Primary Keys:** Use
   `Optional[int] = Field(default=None, primary_key=True)` for auto-increment
   IDs
4. **Commented Foreign Keys:** Foreign key constraints are commented out for
   flexibility during development
5. **Indexes:** Add `index=True` for frequently queried fields
6. **Descriptions:** Always provide field descriptions
7. **Table Names:** Use `__tablename__` to explicitly set table names (usually
   snake_case)
8. **Timestamps:** Use `datetime.utcnow` for creation timestamps (note: consider
   migrating to `datetime.now(datetime.UTC)` to avoid deprecation warning)

### Lookup Tables Pattern

```python
class MyLookup(SQLModel, table=True):
    """Lookup table for my values."""
    __tablename__ = "my_lookup"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, description="Lookup value")
```

## Testing

### Test Structure

Tests are in the `tests/` directory:

- **`conftest.py`**: Shared fixtures (engine, session)
- **`test_biomass.py`**: Tests for biomass models
- **`test_geographic_locations.py`**: Tests for location models
- **`test_package.py`**: Package metadata tests
- **`README.md`**: Test documentation

### Running Tests

```bash
# Run all tests (from main project root)
pixi run pytest src/ca_biositing/datamodels -v

# Run specific test file
pixi run pytest src/ca_biositing/datamodels/tests/test_biomass.py -v

# Run with coverage
pixi run pytest src/ca_biositing/datamodels --cov=ca_biositing.datamodels --cov-report=html
```

### Test Fixtures

From `conftest.py`:

```python
# Use these fixtures in tests
def test_my_model(session):
    """Test using database session."""
    model = MyModel(name="test")
    session.add(model)
    session.commit()
    assert model.id is not None
```

Available fixtures:

- `engine`: SQLite in-memory database engine
- `session`: SQLModel session for database operations

### Writing Tests

**Model Instantiation Test:**

```python
def test_model_creation():
    """Test creating a Model instance."""
    model = MyModel(name="Test", value=Decimal("100.50"))
    assert model.name == "Test"
    assert model.value == Decimal("100.50")
    assert model.id is None  # Not yet persisted
```

**Database Persistence Test:**

```python
def test_model_persistence(session):
    """Test saving and retrieving a Model."""
    model = MyModel(name="Test")
    session.add(model)
    session.commit()
    session.refresh(model)

    assert model.id is not None

    retrieved = session.get(MyModel, model.id)
    assert retrieved is not None
    assert retrieved.name == "Test"
```

## Common Tasks

### Adding a New Model

1. **Choose or create a module** in `ca_biositing/datamodels/`
2. **Define the model class:**

   ```python
   from sqlmodel import SQLModel, Field
   from typing import Optional

   class NewModel(SQLModel, table=True):
       """Description."""
       __tablename__ = "new_model"

       id: Optional[int] = Field(default=None, primary_key=True)
       name: str = Field(default=None, description="Name")
   ```

3. **Write tests** in `tests/test_<module>.py`
4. **Run tests:** `pixi run pytest src/ca_biositing/datamodels -v`
5. **Update migrations** (if needed, see main project Alembic docs)

### Modifying an Existing Model

1. **Understand the change:** Check existing usages in ETL/API code
2. **Update the model:** Modify field definitions
3. **Update tests:** Ensure tests cover the changes
4. **Run tests:** Verify nothing breaks
5. **Generate migration:** Use Alembic to create database migration script (see
   main project workflow)
6. **Update documentation:** If needed, update README.md

### Creating a Migration

Model changes require database migrations:

1. **Make model changes** in the appropriate module
2. **Generate migration** (from main project root):
   ```bash
   # See main project ALEMBIC_WORKFLOW.md
   cd src/ca_biositing/pipeline
   alembic revision --autogenerate -m "description of changes"
   ```
3. **Review migration script** in `alembic/versions/`
4. **Test migration:** Apply and verify in development database
5. **Commit migration** with model changes

## Code Quality & Standards

### Pre-commit Checks

Always run pre-commit before committing:

```bash
# From main project root
pixi run pre-commit run --files src/ca_biositing/datamodels/**/*
```

Or for specific files:

```bash
pixi run pre-commit run --files src/ca_biositing/datamodels/ca_biositing/datamodels/biomass.py
```

### Code Style

- **Type hints:** Required for all fields and functions
- **Docstrings:** Use triple-quoted strings for classes and complex functions
- **Formatting:** Handled by pre-commit (prettier, autopep8, etc.)
- **Line length:** Follow PEP 8 guidelines
- **Imports:** Group by standard library, third-party, local

### Import Conventions

```python
# Standard library
from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

# Third-party
from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# Local (if needed)
# from ca_biositing.datamodels.config import settings
```

## Common Pitfalls & Solutions

### Issue: Import errors with namespace package

**Problem:** Can't import `ca_biositing.datamodels`

**Solution:**

- Ensure `ca_biositing/` does **NOT** have `__init__.py`
- Ensure `ca_biositing/datamodels/` **DOES** have `__init__.py`
- Install package in editable mode: `pip install -e .`
- For main project: `pixi install`

### Issue: SQLModel field defaults

**Problem:** Field validation errors or unexpected None values

**Solution:**

- Use `default=None` for optional fields
- Use `Optional[T]` type hint for nullable fields
- Use `default_factory=callable` for mutable defaults (lists, dicts, datetime)
- Example: `created_at: datetime = Field(default_factory=datetime.utcnow)`

### Issue: Foreign key constraints

**Problem:** Foreign key violations or cascade issues

**Solution:**

- Foreign keys are **commented out** in models for development flexibility
- Uncomment when ready to enforce constraints
- Coordinate with database migrations
- Example:
  ```python
  parent_id: Optional[int] = Field(
      default=None,
      description="Reference to parent"
      # foreign_key="parent_table.id"  # Uncomment when ready
  )
  ```

### Issue: Decimal vs Float

**Problem:** Precision issues with financial/scientific data

**Solution:**

- **Always use `Decimal`** for currency, percentages, precise measurements
- **Use `float`** only for approximate values or when precision loss is
  acceptable
- Example:
  ```python
  price: Optional[Decimal] = Field(default=None)  # Good
  price: Optional[float] = Field(default=None)    # Bad for currency
  ```

### Issue: DateTime deprecation warning

**Problem:** `datetime.utcnow()` deprecation warning

**Current:**

```python
created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Recommended migration:**

```python
from datetime import datetime, UTC

created_at: datetime = Field(
    default_factory=lambda: datetime.now(UTC)
)
```

## Integration with Main Project

### Usage in ETL Pipeline

Models are imported in ETL load modules:

```python
from ca_biositing.datamodels.biomass import Biomass, FieldSample

# In load function
biomass = Biomass(biomass_name="Corn Stover")
session.add(biomass)
session.commit()
```

### Usage in API

Models serve as both ORM and Pydantic models:

```python
from fastapi import APIRouter
from ca_biositing.datamodels.biomass import Biomass

router = APIRouter()

@router.get("/biomass/{biomass_id}")
def get_biomass(biomass_id: int) -> Biomass:
    # Biomass works as both ORM model and response model
    return session.get(Biomass, biomass_id)
```

### Database Migrations

- Migrations are managed in the main project's `pipeline/` directory
- Use Alembic for schema changes
- See main project's `ALEMBIC_WORKFLOW.md` for details

## Best Practices

1. **Namespace Package:** Never add `__init__.py` to `ca_biositing/` directory
2. **Type Safety:** Use proper type hints for all fields
3. **Field Descriptions:** Always document field purpose
4. **Decimal Precision:** Use `Decimal` for precise numeric values
5. **Optional Fields:** Use `Optional[T]` for nullable database columns
6. **Indexes:** Add indexes to frequently queried fields
7. **Table Names:** Explicitly set `__tablename__` (snake_case)
8. **Foreign Keys:** Comment out during development, enable when stable
9. **Timestamps:** Use `default_factory` for datetime fields
10. **Testing:** Write both instantiation and persistence tests
11. **Migrations:** Generate Alembic migrations for schema changes
12. **Documentation:** Keep README.md and docstrings up to date

## Version Information

- **Current Version:** 0.1.0
- **Python:** >= 3.12
- **SQLModel:** >= 0.0.19, < 0.1
- **Alembic:** >= 1.13.2, < 2
- **PostgreSQL:** Supported via psycopg2

## Related Documentation

- **Main Project AGENTS.md:**
  `/Users/lsetiawan/Repos/SSEC/ca-biositing/AGENTS.md`
- **Package README:** `README.md` (in this directory)
- **Test Documentation:** `tests/README.md`
- **Alembic Workflow:** Main project's `pipeline/ALEMBIC_WORKFLOW.md`
- **ETL Workflow:** Main project's `pipeline/ETL_WORKFLOW.md`
- **SQLModel Docs:** <https://sqlmodel.tiangolo.com/>
- **Pydantic Docs:** <https://docs.pydantic.dev/>

## Trust These Instructions

These instructions were generated through analysis of the package structure,
dependencies, and integration patterns. **Follow these guidelines when:**

- Adding or modifying database models
- Writing tests for models
- Integrating models with ETL or API code
- Troubleshooting import or validation issues

**Only search for additional information if:**

- Instructions appear outdated or produce errors
- Working with advanced SQLAlchemy features not covered here
- Implementing new patterns not documented here
- Debugging complex migration issues

For routine model development, testing, and maintenance, these instructions
provide complete guidance.
