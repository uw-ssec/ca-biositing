# Alembic & Materialized View Workflow

## Overview

This document describes the architecture and workflow for managing materialized
views in the ca-biositing project. The key principle is **immutability**: view
definitions are frozen in Alembic migrations as raw SQL strings, never imported
dynamically at upgrade time.

---

## Architecture

### Two-Part System

The project uses a **dual-definition system** for materialized views:

1. **Python View Modules**
   (`src/ca_biositing/datamodels/data_portal_views/mv_*.py`)
   - Pure SQLAlchemy `select()` expressions
   - Used for **development, testing, and documentation**
   - NOT used during migration/deployment
   - Can be freely modified and tested locally

2. **Alembic Migrations** (`alembic/versions/*.py`)
   - Immutable raw SQL strings frozen at the time of creation
   - Used during **deployment and schema evolution**
   - Define the actual database schema
   - Are the single source of truth for the live database

### Why Two Definitions?

This separation prevents a critical class of deployment failures:

- **Problem**: If migrations imported Python view definitions directly,
  upgrading would require running the entire ORM layer during deployment
- **Risk**: Large imports can hang, timeout, or introduce unexpected behavior
- **Solution**: Migrations contain the compiled SQL only, making them fast and
  deterministic

---

## Current Materialized Views

The project has **10 data portal materialized views** managed under this
pattern:

| View Name                      | Purpose                           | Key Columns                                         |
| ------------------------------ | --------------------------------- | --------------------------------------------------- |
| `mv_biomass_search`            | Full-text search on resources     | id, resource_id, search_vector                      |
| `mv_biomass_availability`      | Seasonal availability data        | resource_id, from_month, to_month                   |
| `mv_biomass_composition`       | Analysis data aggregated by type  | id, resource_id, geoid, **county**, analysis_type   |
| `mv_biomass_county_production` | County-level production estimates | id, resource_id, geoid, scenario_name               |
| `mv_biomass_end_uses`          | Product end uses and trends       | resource_id, use_case                               |
| `mv_biomass_fermentation`      | Fermentation experiment results   | id, resource_id, **geoid**, **county**, strain_name |
| `mv_biomass_gasification`      | Gasification experiment results   | id, resource_id, geoid, parameter_name              |
| `mv_biomass_pricing`           | Historical commodity pricing      | id, resource_id, geoid, **county**                  |
| `mv_biomass_sample_stats`      | Sample aggregation statistics     | resource_id, sample_count                           |
| `mv_usda_county_production`    | USDA census data aggregation      | id, resource_id, geoid                              |

**Bold columns** = Added during PR f989683 consolidation (geographic grouping
with `county`)

---

## File Organization

### Python View Modules

```
src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/
├── __init__.py                    # Exports all view objects for backward compatibility
├── mv_biomass_search.py           # SQLAlchemy select() for search view
├── mv_biomass_availability.py     # SQLAlchemy select() for availability view
├── mv_biomass_composition.py      # SQLAlchemy select() for composition view
├── mv_biomass_county_production.py
├── mv_biomass_end_uses.py
├── mv_biomass_fermentation.py
├── mv_biomass_gasification.py
├── mv_biomass_pricing.py
├── mv_biomass_sample_stats.py
└── mv_usda_county_production.py
```

Each module contains:

- SQLAlchemy `select()` expression (pure Python)
- Comments documenting required indexes
- Comments documenting geographic/temporal columns

**Example structure:**

```python
# mv_biomass_composition.py
"""
mv_biomass_composition.py

Compositional analysis data aggregated across different analysis types
(compositional, proximate, ultimate, xrf, icp, calorimetry, xrd, ftnir, pretreatment).

Grouped by resource_id, analysis_type, parameter_name, unit, and geoid from field sample.

Required indexes:
    CREATE INDEX idx_mv_biomass_composition_resource_id ON data_portal.mv_biomass_composition (resource_id)
    CREATE INDEX idx_mv_biomass_composition_geoid ON data_portal.mv_biomass_composition (geoid)
    CREATE INDEX idx_mv_biomass_composition_county ON data_portal.mv_biomass_composition (county)
    CREATE INDEX idx_mv_biomass_composition_analysis_type ON data_portal.mv_biomass_composition (analysis_type)
    ... etc
"""

from sqlalchemy import select, func, union_all, literal
from ca_biositing.datamodels.models.resource_information.resource import Resource
# ... other imports ...

def get_composition_query(model, analysis_type):
    """Generate a select statement for a specific analysis record type with geoid from field sample."""
    return select(
        model.resource_id,
        literal(analysis_type).label("analysis_type"),
        Parameter.name.label("parameter_name"),
        Observation.value.label("value"),
        Unit.name.label("unit"),
        LocationAddress.geography_id.label("geoid")
    ).join(Observation, Observation.record_id == model.record_id)\
     .join(Parameter, Observation.parameter_id == Parameter.id)\
     # ... more joins ...

# ... view definition ...
mv_biomass_composition = select(
    func.row_number().over(...).label("id"),
    all_measurements.c.resource_id,
    # ... columns ...
).select_from(all_measurements)\
 .join(Resource, ...)\
 .group_by(...)
```

### Alembic Migrations

```
alembic/versions/
├── 9e8f7a6b5c54_consolidated_pr_f989683_views_with_geoid.py  # Creates all 10 views with immutable SQL
├── 9e8f7a6b5c52_integrate_pr_f989683_indexes.py              # Creates 27 indexes
└── ... (other migrations)
```

**Key migration:** `9e8f7a6b5c54_consolidated_pr_f989683_views_with_geoid.py`

- Contains complete SQL for all 10 materialized views
- Uses raw SQL strings (`op.execute("""...""")`)
- Includes DROP statements for safe re-creation
- Never imports Python view modules

---

## Workflow: When You Need to Update a View

### Scenario 1: Updating a View Definition

If you need to change a view's logic (e.g., add a column, change filters, fix a
join):

#### Step 1: Edit the Python Module (For Development)

```python
# src/ca_biositing/datamodels/data_portal_views/mv_biomass_composition.py
# Make changes to the SQLAlchemy select() expression
```

#### Step 2: Test Locally

```bash
# Test the view definition works
pixi run python3 << 'EOF'
from ca_biositing.datamodels.data_portal_views import mv_biomass_composition
from sqlalchemy.dialects import postgresql

# Compile to SQL for inspection
sql = str(mv_biomass_composition.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={'literal_binds': True}
))
print(sql)
EOF
```

#### Step 3: Compile to PostgreSQL SQL

```bash
# Generate the compiled SQL string
pixi run python3 << 'EOF'
from ca_biositing.datamodels.data_portal_views import mv_biomass_composition
from sqlalchemy.dialects import postgresql

sql = str(mv_biomass_composition.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={'literal_binds': True}
))

# Copy this output for use in the migration file
print(sql)
EOF
```

#### Step 4: Create a New Alembic Migration

```bash
pixi run alembic revision -m "Update mv_biomass_composition with [description of changes]"
```

This creates:
`alembic/versions/[new_id]_update_mv_biomass_composition_with_[description].py`

#### Step 5: Fill in the Migration

Edit the migration file:

```python
def upgrade() -> None:
    """Drop and recreate mv_biomass_composition with updated logic."""

    # Drop the old view
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")

    # Recreate with new SQL (copied from step 3)
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_composition AS
        SELECT ... (paste the compiled SQL here) ...
    """)

    # Recreate indexes if columns changed
    op.execute("""CREATE INDEX idx_mv_biomass_composition_resource_id ON data_portal.mv_biomass_composition (resource_id)""")
    op.execute("""CREATE INDEX idx_mv_biomass_composition_geoid ON data_portal.mv_biomass_composition (geoid)""")
    # ... etc for all indexes ...

def downgrade() -> None:
    """Drop and restore previous version of mv_biomass_composition."""

    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")

    # Recreate with previous SQL (keep this from git history or manual backup)
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_composition AS
        SELECT ... (previous SQL) ...
    """)

    # Recreate previous indexes
    # ... etc ...
```

#### Step 6: Test the Migration

```bash
# Run migrations
POSTGRES_HOST=localhost pixi run migrate

# Verify view exists and has correct columns
POSTGRES_HOST=localhost pixi run access-db << 'EOF'
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'data_portal'
  AND table_name = 'mv_biomass_composition'
ORDER BY ordinal_position;
EOF

# Verify data is correct
POSTGRES_HOST=localhost pixi run access-db << 'EOF'
SELECT * FROM data_portal.mv_biomass_composition LIMIT 5;
EOF
```

#### Step 7: Commit and Push

```bash
git add alembic/versions/[new_migration_file]
git add src/ca_biositing/datamodels/data_portal_views/mv_biomass_composition.py
git commit -m "Update mv_biomass_composition: [description]"
git push origin [branch]
```

---

### Scenario 2: Adding a New Materialized View

#### Step 1: Create a Python Module

```python
# src/ca_biositing/datamodels/data_portal_views/mv_new_view.py
"""
mv_new_view.py

Description of the view's purpose and use case.

Required indexes:
    CREATE UNIQUE INDEX idx_mv_new_view_id ON data_portal.mv_new_view (id)
    ... etc
"""

from sqlalchemy import select, func
from ca_biositing.datamodels.models import ...

mv_new_view = select(
    func.row_number().over(order_by=(...)).label("id"),
    # ... columns ...
).select_from(...)\
 .join(...)\
 .group_by(...)
```

#### Step 2: Update `__init__.py`

```python
# src/ca_biositing/datamodels/data_portal_views/__init__.py
from .mv_new_view import mv_new_view

__all__ = [
    'mv_biomass_search',
    # ... existing views ...
    'mv_new_view',  # Add here
]
```

#### Step 3: Compile to SQL

```bash
pixi run python3 << 'EOF'
from ca_biositing.datamodels.data_portal_views import mv_new_view
from sqlalchemy.dialects import postgresql

sql = str(mv_new_view.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={'literal_binds': True}
))
print(sql)
EOF
```

#### Step 4: Create Migration

```bash
pixi run alembic revision -m "Add mv_new_view materialized view"
```

#### Step 5: Fill in Migration

```python
def upgrade() -> None:
    """Create mv_new_view materialized view."""

    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_new_view AS
        SELECT ... (compiled SQL) ...
    """)

    # Create indexes
    op.execute("""CREATE UNIQUE INDEX idx_mv_new_view_id ON data_portal.mv_new_view (id)""")
    op.execute("""CREATE INDEX idx_mv_new_view_resource_id ON data_portal.mv_new_view (resource_id)""")
    # ... etc ...

def downgrade() -> None:
    """Drop mv_new_view materialized view."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_new_view CASCADE")
```

#### Step 6: Test and Commit (as above)

---

## Important Rules

### ✓ DO

1. **Edit Python view modules freely** - they are for development and testing
2. **Compile to SQL before creating migrations** - ensures the SQL is what you
   tested
3. **Use raw SQL strings in migrations** - immutability is the goal
4. **Include DROP statements** - allows safe re-creation during migration
5. **Create separate migrations for view changes** - one view per migration for
   clarity
6. **Document required indexes in Python modules** - helps future developers
7. **Test migrations locally** - run `pixi run migrate` before pushing

### ✗ DON'T

1. **Do NOT import Python view modules in migrations** - defeats the
   immutability purpose
2. **Do NOT embed Python code in migrations** - migrations must be deterministic
3. **Do NOT modify migrations after they've been deployed** - immutability is
   the contract
4. **Do NOT manually craft SQL without testing** - compile from Python first
5. **Do NOT forget to test migrations locally** - migrations are permanent

---

## Example: The PR f989683 Consolidation

The recent migration consolidation (PR f989683) exemplifies this workflow:

**Before:**

- 3 separate migration files with broken/incomplete SQL
- Syntax errors and truncated view definitions
- Missing geographic (county) columns in some views

**Solution:**

1. Read all 10 Python view modules
2. Compiled each to PostgreSQL SQL
3. Created consolidated migration `9e8f7a6b5c54` with all 10 views as raw SQL
4. Fixed errors identified during compilation
5. Added missing columns (county) by extending the SQL
6. Created index migration `9e8f7a6b5c52` to handle all 27 indexes
7. Tested end-to-end: `pixi run migrate`
8. Verified all views exist and have correct data

This approach ensures:

- All SQL is reviewed and tested before deployment
- No dynamic imports during upgrade
- Easy rollback via downgrade migrations
- Clear audit trail of schema changes

---

## Refreshing Materialized Views (Post-Migration)

After views are created or updated, refresh their data:

```bash
# Refresh all data portal views
pixi run refresh-views

# Or refresh manually
POSTGRES_HOST=localhost pixi run access-db << 'EOF'
REFRESH MATERIALIZED VIEW CONCURRENTLY data_portal.mv_biomass_search;
REFRESH MATERIALIZED VIEW CONCURRENTLY data_portal.mv_biomass_composition;
-- ... etc for all views ...
EOF
```

Note: Use `CONCURRENTLY` only if the view has a UNIQUE index (supports
concurrent refresh without locking).

---

## Related Documentation

- **Migration Consolidation Summary**:
  `docs/pr/PR_f989683_migration_consolidation.md`
- **Detailed Handoff Document**:
  `plans/migration_consolidation_handoff_phase6.md`
- **Initial Refactor Plan**: `plans/data_portal_view_refactor_simple.md`
- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **SQLAlchemy Compilation**:
  https://docs.sqlalchemy.org/en/20/faq/sql_expressions.html#how-do-i-construct-a-textual-sql-fragment-that-is-database-specific

---

## FAQ

**Q: Why can't I just modify the Alembic migration file to import the Python
view?** A: Because migrations run during deployment when imports can hang. Raw
SQL is fast and deterministic.

**Q: What if I make a mistake in the Python module?** A: That's fine! Test it,
fix it, then compile again and create a new migration. The Python module is for
development.

**Q: Do I have to manually compile to SQL every time?** A: Yes, currently. This
ensures you review the generated SQL before committing. Future enhancements
could automate this.

**Q: What if I forget to update the Python module when creating a migration?**
A: That's okay if you only changed the SQL. But for clarity, update both. The
Python module documents the view's intended structure.

**Q: How do I rollback a view change?** A: Run `pixi run alembic downgrade -1`
to revert to the previous migration, which recreates the old view.

**Q: Can I have two versions of a view?** A: No, but you can create a new view
with a new name and deprecate the old one over time.

**Q: Do I need to refresh views after every migration?** A: Not after
creation/alteration (schema changes). But yes if the underlying data has changed
and you need fresh results.

---

## Summary

The dual-definition system (Python modules + Alembic migrations) provides:

- **Safety**: Immutable migrations prevent runtime surprises
- **Clarity**: Raw SQL is explicit and reviewable
- **Flexibility**: Python modules let developers experiment locally
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new views or update existing ones

Always remember: **The Alembic migration is the source of truth for the live
database.**
