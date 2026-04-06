# Alembic Migrations Guide for Agents

This guide provides instructions for working with Alembic migrations in the
ca-biositing project, particularly for materialized view updates.

## Data Portal Views Refactoring

After the data portal views refactor, all materialized views are defined as
SQLAlchemy expressions in:

```
src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/
├── __init__.py                          # Backward compatibility re-exports
├── common.py                            # Shared subqueries and expressions
├── mv_biomass_availability.py
├── mv_biomass_search.py
├── mv_biomass_composition.py
├── mv_biomass_county_production.py
├── mv_biomass_sample_stats.py
├── mv_biomass_fermentation.py
├── mv_biomass_gasification.py
├── mv_biomass_pricing.py
└── mv_usda_county_production.py
```

### Updating a Materialized View

**IMPORTANT: Use Raw SQL Snapshots (See Below)**

When you need to update a materialized view:

1. **Modify the view definition** in its module (e.g., `mv_biomass_search.py`)
2. **Extract the compiled SQL** from the SQLAlchemy expression
3. **Embed raw SQL as a string** in the migration file (immutable snapshot)
4. **Run the migration** to deploy changes to the database

### Why Raw SQL Snapshots?

SQLAlchemy-generated migrations work fine until you need to **teardown volumes
and replay from scratch**. When that happens:

- ❌ Importing SQLAlchemy models at replay time uses **current** definitions
- ❌ If schema changed since migration was created, the view fails to build
- ❌ Migration chain breaks, preventing database recreation

**Solution: Embed raw SQL as immutable strings**

- ✅ Migration is frozen at creation time
- ✅ Replays always work, even with future schema changes
- ✅ Industry standard (Liquibase, Flyway, all major Alembic projects)
- ✅ Full audit trail of what SQL was run when

### Template: Update Materialized View with Raw SQL (RECOMMENDED)

```python
"""update_mv_biomass_search

Update the mv_biomass_search view with new logic using raw SQL snapshot.

Revision ID: YOUR_REVISION_ID
Revises: PREVIOUS_REVISION_ID
Create Date: 2026-04-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'YOUR_REVISION_ID'
down_revision = 'PREVIOUS_REVISION_ID'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Update mv_biomass_search with immutable SQL snapshot."""

    # Drop the old view (CASCADE handles dependent views)
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")

    # Create the view with raw SQL snapshot
    # This SQL was compiled from SQLAlchemy at migration-creation time
    # and is frozen here for all future replays (immutable, not runtime-evaluated)
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
        SELECT ... (complete SQL from `scripts/extract_view_sql.py` output)
    """)

    # Recreate the unique index for performance
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_search_id
        ON data_portal.mv_biomass_search (id)
    """)

    # Grant select to readonly user
    op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")


def downgrade() -> None:
    """Downgrade: drop the view."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
```

### Extracting Raw SQL for Migrations

Use the extraction script to get compiled SQL:

```bash
# Extract all view SQL
pixi run python scripts/extract_view_sql.py

# Copy the SQL output and embed it in your migration file
# See alembic/versions/9e8f7a6b5c4e_recreate_mv_biomass_search_with_raw_sql.py
# for a complete example
```

### Template: Legacy Pattern (DON'T USE - for reference only)

If you encounter old migrations that import SQLAlchemy models, be aware this
pattern is fragile:

```python
"""update_mv_biomass_search (LEGACY - don't use for new migrations)

This pattern should not be used for new migrations because it's not
safe for teardown→rebuild scenarios.

"""
from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import mv_biomass_search

def upgrade() -> None:
    """Legacy: compiles SQLAlchemy at migration time (fragile)."""
    # ❌ NOT RECOMMENDED: future schema changes break this migration
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")

    compiled = mv_biomass_search.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {compiled}")
```

### Key Patterns

**Pattern 1: Raw SQL Snapshot (RECOMMENDED)**

Embed SQL as an immutable string in the migration:

```python
def upgrade() -> None:
    """Update view with raw SQL snapshot."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")

    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
        SELECT ... (raw SQL here - extracted via scripts/extract_view_sql.py)
    """)

    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_search_id
        ON data_portal.mv_biomass_search (id)
    """)

    op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")
```

**Pattern 2: Compile SQLAlchemy at Migration Time (LEGACY - don't use for new
migrations)**

This pattern is fragile for teardown→rebuild scenarios:

```python
from ca_biositing.datamodels.data_portal_views import mv_biomass_search

def upgrade() -> None:
    """Legacy pattern - fragile, not recommended."""
    compiled = mv_biomass_search.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {compiled}")
```

**Index creation (view-specific):**

```python
# Check the view module's docstring for the required index
# Example for mv_biomass_search:
op.execute("""
CREATE UNIQUE INDEX idx_mv_biomass_search_id
ON data_portal.mv_biomass_search (id)
""")
```

**Grant readonly access:**

```python
op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")
```

### View Index Requirements

Each view module has a docstring documenting required indexes. Examples:

**mv_biomass_search:**

```
CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)
```

**mv_biomass_composition:**

```
CREATE UNIQUE INDEX idx_mv_biomass_composition_key
ON data_portal.mv_biomass_composition (resource_id, analysis_type, parameter_name, unit)
```

### Testing Migrations Locally

Always test migrations against a running database:

```bash
# Start services
pixi run start-services

# Run migrations
pixi run migrate

# Verify the view exists
pixi run access-db -c "SELECT * FROM data_portal.mv_biomass_search LIMIT 1;"
```

### Immutable SQL Snapshots

When a migration compiles a SQLAlchemy expression to SQL, that SQL becomes the
**authoritative definition** for the view in the database at that point in time.

Key points:

- ✅ If the Python code changes later, the database retains the original SQL
- ✅ The compiled SQL is immutable per migration
- ✅ Future changes require new migrations
- ✅ Full audit trail via migration history

### SQL Reference Documentation

For permanent records of compiled SQL, include it in migration docstrings:

```python
def upgrade() -> None:
    """
    Update mv_biomass_search.

    Compiled SQL snapshot (for reference):
    CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
      SELECT ... (full SQL here) ...
    """
```

For periodic full database snapshots, use pgschema:

```bash
pixi run schema-dump
# Exports current schema to exports/ for reference
```

## Related Documentation

- **View Refactor Guide**: `docs/datamodels/DATA_PORTAL_VIEWS_REFACTOR.md`
- **Alembic Workflow**: `docs/pipeline/ALEMBIC_WORKFLOW.md`
- **SQL-First Workflow**: `docs/datamodels/SQL_FIRST_WORKFLOW.md`
