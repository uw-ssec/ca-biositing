# Namespace Package Migration Guide

## Overview

This guide explains the namespace package restructuring completed in Phase 1 and provides instructions for developers working with the new structure.

## What Changed

### Before (Old Structure)
```
src/
├── ca_biositing/
│   ├── __init__.py          # Regular package
│   ├── api/
│   └── hello.py
└── pipeline/
    ├── models/              # Database models (duplicate 1)
    ├── etl/
    │   └── models/          # Database models (duplicate 2)
    ├── database.py
    └── flows/
```

### After (New Structure - PEP 420 Namespace)
```
src/
└── ca_biositing/            # PEP 420 implicit namespace (no __init__.py)
    ├── datamodels/          # Shared data models package
    │   ├── __init__.py
    │   ├── pyproject.toml
    │   ├── README.md
    │   ├── config.py
    │   ├── database.py
    │   ├── biomass.py
    │   ├── experiments_analysis.py
    │   └── ... (all model files)
    ├── pipeline/            # ETL pipeline package
    │   ├── __init__.py
    │   ├── pyproject.toml
    │   ├── etl/
    │   ├── flows/
    │   └── utils/
    └── api/                 # API package (unchanged)
```

## Key Changes

1. **Implicit Namespace**: `ca_biositing` is now a PEP 420 implicit namespace package (no `__init__.py`)
2. **Consolidated Models**: All database models moved to `ca_biositing.datamodels`
3. **Removed Duplicates**: Eliminated duplicate model directories
4. **Separate Packages**: Both `datamodels` and `pipeline` are independently installable

## Import Changes

### Old Imports
```python
# Models
from src.pipeline.models.biomass import FieldSample
from src.pipeline.etl.models.biomass import PrimaryProduct

# Database
from src.pipeline.database import engine

# ETL
from src.pipeline.flows.primary_product import primary_product_flow
```

### New Imports
```python
# Models
from ca_biositing.datamodels.biomass import FieldSample, PrimaryProduct

# Database
from ca_biositing.datamodels.database import engine

# ETL
from ca_biositing.pipeline.flows.primary_product import primary_product_flow
```

## Installation

### Option 1: Editable Install (Development)
```bash
# Install datamodels package
pip install -e src/ca_biositing/datamodels

# Install pipeline package
pip install -e src/ca_biositing/pipeline
```

### Option 2: Using Pixi (Recommended)
```bash
# Install all dependencies
pixi install

# Set PYTHONPATH for development
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Option 3: Full Project Install
```bash
# This will install both packages as dependencies
pip install -e .
```

## Testing

### Run Namespace Verification
```bash
PYTHONPATH=src python3 -c "
from ca_biositing import datamodels
from ca_biositing import pipeline
print(f'✓ datamodels {datamodels.__version__}')
print(f'✓ pipeline {pipeline.__version__}')
"
```

### Run Test Suite
```bash
# With pixi
pixi run test

# Or with pytest directly
PYTHONPATH=src pytest tests/ -v
```

## Database Configuration

The database configuration has been consolidated in `ca_biositing.datamodels.config`:

```python
from ca_biositing.datamodels.config import config

# Configuration uses Pydantic Settings
# Can be set via environment variables or .env file
DATABASE_URL=postgresql://user:password@localhost:5432/ca_biositing
```

## Alembic Migrations

Alembic configuration has been updated to use the new import paths:

```bash
# Check migrations
alembic check

# Run migrations
alembic upgrade head

# Generate new migration
python generate_migration.py
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError
**Problem**: `ModuleNotFoundError: No module named 'ca_biositing.datamodels'`

**Solution**: Ensure PYTHONPATH includes the src directory:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Issue 2: Import Errors in Tests
**Problem**: Tests failing with import errors

**Solution**: Update test imports to use new namespace:
```python
# Old
from pipeline.models.biomass import Biomass
from pipeline.database import engine

# New
from ca_biositing.datamodels.biomass import Biomass
from ca_biositing.datamodels.database import engine
```

### Issue 3: Alembic Can't Find Models
**Problem**: Alembic can't generate migrations

**Solution**: The `alembic/env.py` file has been updated. Ensure you're using the latest version that imports from `ca_biositing.datamodels.*`

## Docker Usage

If using Docker for the ETL pipeline, ensure your Dockerfile includes:

```dockerfile
# Install packages in editable mode
RUN pip install -e /app/src/ca_biositing/datamodels
RUN pip install -e /app/src/ca_biositing/pipeline

# Or set PYTHONPATH
ENV PYTHONPATH=/app/src
```

## Benefits of This Structure

1. **Clear Separation**: Models, pipeline, and API are clearly separated
2. **Reusability**: Models can be imported independently in other projects
3. **No Duplication**: Single source of truth for all database models
4. **PEP 420 Compliance**: Uses modern Python namespace package standards
5. **Independent Versioning**: Each package can be versioned independently

## Files Changed

### Created
- `src/ca_biositing/datamodels/__init__.py`
- `src/ca_biositing/datamodels/pyproject.toml`
- `src/ca_biositing/datamodels/README.md`
- `src/ca_biositing/datamodels/config.py`
- `src/ca_biositing/datamodels/database.py` (refactored)
- `src/ca_biositing/pipeline/pyproject.toml`
- `src/ca_biositing/version.py`
- `tests/test_namespace_imports.py`

### Moved
- All model files from `src/pipeline/models/` → `src/ca_biositing/datamodels/`
- All pipeline files from `src/pipeline/` → `src/ca_biositing/pipeline/`

### Deleted
- `src/ca_biositing/__init__.py` (to create implicit namespace)
- `src/pipeline/models/` (duplicate)
- `src/pipeline/etl/models/` (duplicate)
- `src/pipeline/etl/database.py` (duplicate)

### Updated
- `alembic/env.py` - imports from `ca_biositing.datamodels`
- `generate_migration.py` - imports from `ca_biositing.datamodels`
- `run_prefect_flow.py` - imports from `ca_biositing.pipeline`
- All ETL extract/transform/load modules
- All Prefect flow files
- Test files

## Next Steps

1. Update any custom scripts or notebooks to use new import paths
2. Update CI/CD pipelines if needed
3. Test Alembic migrations in development environment
4. Test Prefect flows with new imports
5. Update documentation and README files
6. Consider adding type hints and improving docstrings

## Questions?

If you have questions about this migration, please refer to:
- [PEP 420 - Implicit Namespace Packages](https://www.python.org/dev/peps/pep-0420/)
- [Scientific Python Development Guide](https://learn.scientific-python.org/development/)
- Project issue #54 for context
