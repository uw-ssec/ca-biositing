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

## Cross-Cutting Documentation

This package follows project-wide patterns documented in:

| Topic              | Document                                                           | When to Reference                          |
| ------------------ | ------------------------------------------------------------------ | ------------------------------------------ |
| Namespace Packages | [namespace_packages.md](../../../agent_docs/namespace_packages.md) | Import errors, package structure questions |
| Testing Patterns   | [testing_patterns.md](../../../agent_docs/testing_patterns.md)     | Writing tests, fixtures, pytest commands   |
| Code Quality       | [code_quality.md](../../../agent_docs/code_quality.md)             | Pre-commit, style, imports                 |
| Troubleshooting    | [troubleshooting.md](../../../agent_docs/troubleshooting.md)       | Common errors and solutions                |

## Dependencies

From `pyproject.toml`:

- **SQLModel** (>=0.0.19, <0.1): SQL database ORM with type hints
- **Alembic** (>=1.13.2, <2): Database migrations
- **psycopg2** (>=2.9.9, <3): PostgreSQL adapter
- **Pydantic** (>=2.0.0): Data validation
- **Pydantic Settings** (>=2.0.0): Configuration management

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
8. **Timestamps:** Use `default_factory=datetime.utcnow` for creation timestamps

### Lookup Tables Pattern

```python
class MyLookup(SQLModel, table=True):
    """Lookup table for my values."""
    __tablename__ = "my_lookup"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, description="Lookup value")
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
5. **Update migrations** (if needed, see Alembic workflow)

### Modifying an Existing Model

1. **Understand the change:** Check existing usages in ETL/API code
2. **Update the model:** Modify field definitions
3. **Update tests:** Ensure tests cover the changes
4. **Run tests:** Verify nothing breaks
5. **Generate migration:** Use Alembic to create database migration script
6. **Update documentation:** If needed, update README.md

### Creating a Migration

Model changes require database migrations:

1. **Make model changes** in the appropriate module
2. **Generate migration** (from main project root):
   ```bash
   pixi run exec-prefect-worker alembic revision --autogenerate -m "description of changes"
   ```
3. **Review migration script** in `alembic/versions/`
4. **Test migration:** Apply and verify in development database
5. **Commit migration** with model changes

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

- **Main Project AGENTS.md:** [/AGENTS.md](../../../AGENTS.md)
- **Package README:** `README.md` (in this directory)
- **Test Documentation:** `tests/README.md`
- **Alembic Workflow:** `docs/pipeline/ALEMBIC_WORKFLOW.md`
- **SQLModel Docs:** <https://sqlmodel.tiangolo.com/>
- **Pydantic Docs:** <https://docs.pydantic.dev/>
