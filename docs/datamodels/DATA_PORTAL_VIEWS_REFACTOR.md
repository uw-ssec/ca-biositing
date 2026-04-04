# Data Portal Views Refactor: Complete Guide

## Overview

The data portal materialized views have been refactored from a monolithic
`data_portal_views.py` file into a modular package structure for better
maintainability and clarity.

**Old Structure:**

```
src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views.py  (521 lines)
```

**New Structure:**

```
src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/
├── __init__.py                          # Backward compatibility re-exports
├── common.py                            # Shared subqueries and expressions
├── mv_biomass_availability.py           # View: Resource availability
├── mv_biomass_search.py                 # View: Comprehensive biomass search
├── mv_biomass_composition.py            # View: Compositional analysis data
├── mv_biomass_county_production.py      # View: County-level production
├── mv_biomass_sample_stats.py           # View: Sample statistics
├── mv_biomass_fermentation.py           # View: Fermentation analysis
├── mv_biomass_gasification.py           # View: Gasification analysis
├── mv_biomass_pricing.py                # View: Market pricing data
└── mv_usda_county_production.py         # View: USDA Census data
```

## Backward Compatibility

✅ **Full backward compatibility maintained**

Existing code can continue using the original import patterns:

```python
# Old style (still works!)
from ca_biositing.datamodels.data_portal_views import mv_biomass_search

# New style (recommended)
from ca_biositing.datamodels.data_portal_views import mv_biomass_search
```

Both import paths resolve to the same view definition. The `__init__.py`
re-exports all views, ensuring existing code continues to work without
modifications.

## Key Components

### 1. Common Module (`common.py`)

Contains shared subqueries and expressions used by multiple views:

**Subqueries:**

- `analysis_metrics`: Aggregated analytical metrics (moisture, ash, lignin,
  etc.)
- `resource_analysis_map`: Union of all record types mapped to resource_id

**Expressions:**

- `carbon_avg_expr`: Average carbon percentage from ultimate analysis
- `hydrogen_avg_expr`: Average hydrogen percentage from ultimate analysis
- `nitrogen_avg_expr`: Average nitrogen percentage from ultimate analysis
- `cn_ratio_expr`: Carbon-to-nitrogen ratio expression

**Usage in View Modules:**

```python
from .common import analysis_metrics, resource_analysis_map, carbon_avg_expr
```

### 2. View Modules

Each view is in its own module with:

- Docstring describing the view purpose
- Required index statement in comments
- Complete SQLAlchemy `select()` expression
- All necessary imports

**Example (`mv_biomass_availability.py`):**

```python
"""
Aggregates resource availability data (months, residue factors).

Required index:
    CREATE UNIQUE INDEX idx_mv_biomass_availability_resource_id
    ON data_portal.mv_biomass_availability (resource_id)
"""

from sqlalchemy import select, func
from ca_biositing.datamodels.models.resource_information.resource import Resource
from ca_biositing.datamodels.models.resource_information.resource_availability import ResourceAvailability

mv_biomass_availability = select(
    Resource.id.label("resource_id"),
    # ... column definitions
).select_from(ResourceAvailability)\
 .join(Resource, ...)\
 .group_by(...)
```

## Working with Views

### Updating a View

When you need to modify a materialized view definition:

1. **Edit the view module** (e.g., `mv_biomass_search.py`)
   - Modify the `select()` expression
   - Update imports if needed
   - Test locally with Python imports

2. **Create a migration** using the template pattern:

   ```bash
   pixi run alembic revision -m "Update mv_biomass_search view for new column"
   ```

3. **Use the migration template** from
   [`alembic/versions/9e8f7a6b5c4d_example_update_mv_biomass_search_view.py`](../../alembic/versions/9e8f7a6b5c4d_example_update_mv_biomass_search_view.py):

   ```python
   def upgrade() -> None:
       """Upgrade: Refresh mv_biomass_search after changes."""
       # Compile the view to SQL
       compiled = mv_biomass_search.compile(
           dialect=sa.dialects.postgresql.dialect(),
           compile_kwargs={"literal_binds": True}
       )

       # Drop and recreate
       op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
       op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {compiled}")

       # Recreate index
       op.execute("CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)")
   ```

4. **Apply the migration:**

   ```bash
   pixi run migrate
   ```

5. **Refresh dependent views** if needed:
   ```bash
   pixi run refresh-views
   ```

### Adding a New View

To add a new data portal view:

1. Create a new module:
   `src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_your_view.py`

2. Define the view with complete docstring and index statement:

   ```python
   """
   mv_your_view - Brief description

   Required index:
       CREATE UNIQUE INDEX idx_mv_your_view_id ON data_portal.mv_your_view (id)
   """

   from sqlalchemy import select
   from ca_biositing.datamodels.models import ...

   mv_your_view = select(
       # ... columns
   )
   ```

3. Add import to `__init__.py`:

   ```python
   from .mv_your_view import mv_your_view
   __all__ = [
       # ... existing views
       "mv_your_view",
   ]
   ```

4. Create migration to create the view (use template pattern)

## Migration Strategy: SQL Snapshots

### Compiling SQLAlchemy to SQL

When you update a view, the migration compiles the SQLAlchemy expression to SQL:

```python
from ca_biositing.datamodels.data_portal_views import mv_biomass_search
import sqlalchemy as sa

compiled = mv_biomass_search.compile(
    dialect=sa.dialects.postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
)
sql = str(compiled)
```

This creates an **immutable snapshot** of the SQL at migration time. Even if the
Python code changes later, the deployed database uses the exact SQL from when
the migration was created.

### Reference Strategy

**Store compiled SQL in migration files as comments:**

```python
def upgrade() -> None:
    """Upgrade: Refresh mv_biomass_search.

    Compiled SQL snapshot (for reference):
    CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
      SELECT ... (full SQL here) ...
    """
```

This provides:

- ✅ Permanent record of what was deployed
- ✅ Easy reference for debugging
- ✅ Traceability of changes over time
- ✅ No dependency on Python code history

**For additional reference snapshots**, use pgschema:

```bash
pixi run schema-dump
```

This exports current database schema to SQL files in `exports/` for periodic
snapshots.

## Testing

### Test Imports Locally

Verify backward compatibility without a running database:

```bash
pixi run python -c "
from ca_biositing.datamodels.data_portal_views import (
    mv_biomass_search,
    mv_biomass_composition,
    # ... other views
)
print('All imports successful!')
"
```

### Test in Migrations

Always test migrations against a running database:

```bash
# Start services
pixi run start-services

# Wait for database to be ready
pixi run service-status

# Apply migration
pixi run migrate

# Check result
pixi run access-db "SELECT COUNT(*) FROM data_portal.mv_biomass_search"
```

## Package Structure Benefits

✅ **Modularity**: Each view in its own file for easier navigation ✅
**Maintainability**: Smaller, focused files are easier to understand and modify
✅ **Reusability**: `common.py` enables shared subqueries across views ✅
**Backward Compatibility**: No breaking changes to existing imports ✅ **Clear
Dependencies**: Imports show exactly what each view needs ✅ **Documentation**:
Each view has its own docstring with index requirements ✅ **Immutable
Snapshots**: SQL compiled at migration time, not runtime

## Troubleshooting

### Import Errors

**Problem:**
`ModuleNotFoundError: No module named 'ca_biositing.datamodels.data_portal_views.mv_biomass_search'`

**Solution:** Ensure Pixi environment is installed:

```bash
pixi install
```

### SQLAlchemy Type Errors

**Problem:** Pylance errors about `.label()` or column types

**Solution:** These are benign type-checking issues from SQLAlchemy's complex
typing. The code runs correctly at runtime. If needed, disable in your IDE or
upgrade SQLAlchemy/Pylance.

### Database Connection Errors

**Problem:**
`psycopg2.OperationalError: could not translate host name "db" to address`

**Solution:** Set `POSTGRES_HOST=localhost` for local development:

```bash
POSTGRES_HOST=localhost pixi run migrate
```

## Implementation Summary

**Phase 1: Package Structure** ✅

- Created modular package with 10 view modules
- Extracted shared subqueries to `common.py`
- Maintained backward compatibility through `__init__.py`

**Phase 2: Import Testing** ✅

- Verified all imports work correctly
- Fixed SQLAlchemy syntax issues
- Tested backward compatibility

**Phase 3: Migration Template** ✅

- Created example migration pattern
- Demonstrates DROP + CREATE approach
- Includes documentation for SQL snapshots

**Phase 4: Documentation** ✅

- Comprehensive guide for view updates
- Clear patterns for adding new views
- Testing and troubleshooting instructions

## Summary

The data portal views refactor is complete and production-ready. The new package
structure provides:

- **Better code organization** through modular files
- **Easier maintenance** with smaller, focused modules
- **Complete backward compatibility** with existing code
- **Clear migration pattern** for future updates
- **SQL snapshot strategy** for immutable deployment records
- **Comprehensive documentation** for future agents

**No breaking changes. No code updates required for existing imports.** Views
work exactly as before, just organized better.
