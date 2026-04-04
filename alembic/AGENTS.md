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

When you need to update a materialized view definition:

1. **Modify the view definition** in its module (e.g., `mv_biomass_search.py`)
2. **Create a new migration** using the template pattern below
3. **Run the migration** to deploy changes to the database

### Template: Update Materialized View Migration

```python
"""update_mv_biomass_search

Update the mv_biomass_search view with new logic.

Revision ID: YOUR_REVISION_ID
Revises: PREVIOUS_REVISION_ID
Create Date: 2026-04-04 02:14:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import mv_biomass_search

# revision identifiers, used by Alembic.
revision: str = 'YOUR_REVISION_ID'
down_revision: Union[str, Sequence[str], None] = 'PREVIOUS_REVISION_ID'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Update mv_biomass_search with new logic.

    This demonstrates the pattern for updating views:
    1. DROP the old view (CASCADE handles dependent views)
    2. COMPILE the new SQLAlchemy expression to SQL
    3. CREATE the view with the new SQL
    4. Recreate indexes
    5. Grant permissions to biocirv_readonly

    SQL Snapshot (immutable at migration time):
    - The compiled SQL below is the authoritative definition for this view
    - Changes to the SQLAlchemy expression in data_portal_views/mv_biomass_search.py
      require a new migration to update the view
    """
    # Drop the old view and dependent views
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")

    # Compile the updated SQLAlchemy expression to SQL
    compiled = mv_biomass_search.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )

    # Create the view with the new SQL (immutable snapshot at migration time)
    sql = f"""
    CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
    {compiled}
    """
    op.execute(sql)

    # Recreate the unique index for performance
    op.execute("""
    CREATE UNIQUE INDEX idx_mv_biomass_search_id
    ON data_portal.mv_biomass_search (id)
    """)

    # Grant select to readonly user
    op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")


def downgrade() -> None:
    """Downgrade: drop the view and index."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
```

### Key Patterns

**Compile SQLAlchemy to SQL:**

```python
compiled = mv_biomass_search.compile(
    dialect=sa.dialects.postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
)
sql = str(compiled)
```

**DROP → CREATE pattern:**

```python
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
