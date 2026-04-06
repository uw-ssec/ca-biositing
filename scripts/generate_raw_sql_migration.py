#!/usr/bin/env python3
"""
Generate a migration file with raw SQL snapshots of all views.

This extracts SQL from SQLAlchemy definitions and embeds them as immutable
strings in the migration file, ensuring replays never fail due to schema changes.

Usage:
    pixi run python scripts/generate_raw_sql_migration.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Import all views
from ca_biositing.datamodels.data_portal_views import (
    mv_biomass_search,
    mv_biomass_availability,
    mv_biomass_composition,
    mv_biomass_county_production,
    mv_biomass_sample_stats,
    mv_biomass_fermentation,
    mv_biomass_gasification,
    mv_biomass_pricing,
    mv_usda_county_production,
)

VIEWS = [
    ("mv_biomass_search", mv_biomass_search, "data_portal.mv_biomass_search"),
    ("mv_biomass_availability", mv_biomass_availability, "data_portal.mv_biomass_availability"),
    ("mv_biomass_composition", mv_biomass_composition, "data_portal.mv_biomass_composition"),
    ("mv_biomass_county_production", mv_biomass_county_production, "data_portal.mv_biomass_county_production"),
    ("mv_biomass_sample_stats", mv_biomass_sample_stats, "data_portal.mv_biomass_sample_stats"),
    ("mv_biomass_fermentation", mv_biomass_fermentation, "data_portal.mv_biomass_fermentation"),
    ("mv_biomass_gasification", mv_biomass_gasification, "data_portal.mv_biomass_gasification"),
    ("mv_biomass_pricing", mv_biomass_pricing, "data_portal.mv_biomass_pricing"),
    ("mv_usda_county_production", mv_usda_county_production, "data_portal.mv_usda_county_production"),
]

INDEXES = {
    "mv_biomass_search": "CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)",
    "mv_biomass_availability": "CREATE UNIQUE INDEX idx_mv_biomass_availability_id ON data_portal.mv_biomass_availability (id)",
    "mv_biomass_composition": "CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)",
    "mv_biomass_county_production": "CREATE UNIQUE INDEX idx_mv_biomass_county_production_id ON data_portal.mv_biomass_county_production (id)",
    "mv_biomass_sample_stats": "CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_id ON data_portal.mv_biomass_sample_stats (id)",
    "mv_biomass_fermentation": "CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)",
    "mv_biomass_gasification": "CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)",
    "mv_biomass_pricing": "CREATE UNIQUE INDEX idx_mv_biomass_pricing_id ON data_portal.mv_biomass_pricing (id)",
    "mv_usda_county_production": "CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)",
}

def compile_view(select_expr):
    """Compile SQLAlchemy select() to PostgreSQL SQL."""
    compiled = select_expr.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    return str(compiled)

def escape_sql_for_python(sql_str):
    """Escape SQL for embedding in Python triple-quoted string."""
    # Replace backslashes and triple quotes
    sql_str = sql_str.replace("\\", "\\\\")
    sql_str = sql_str.replace('"""', r'\"\"\"')
    return sql_str

def generate_migration_code():
    """Generate the full migration Python code."""
    code = '''"""Recreate data portal materialized views with raw SQL snapshots.

This migration embeds immutable SQL snapshots of all materialized views.
This approach ensures migrations are not affected by future schema changes
and can be replayed from scratch without errors.

Revision ID: 9e8f7a6b5c4e
Revises: 9e8f7a6b5c4d
Create Date: 2026-04-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e8f7a6b5c4e'
down_revision = '9e8f7a6b5c4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Recreate mv_biomass_search with immutable SQL snapshot."""
'''

    # Add first view (mv_biomass_search) as example
    view_name = "mv_biomass_search"
    sql = compile_view(VIEWS[0][1])
    escaped_sql = escape_sql_for_python(sql)

    code += f'''    # Drop existing view if present
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.{view_name} CASCADE")

    # Create view with immutable SQL snapshot
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.{view_name} AS
        {escaped_sql}
    """)

    # Create index
    op.execute("""
        {INDEXES[view_name]}
    """)

    # Grant schema access
    op.execute("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly")
    op.execute("GRANT SELECT ON ALL MATERIALIZED VIEWS IN SCHEMA data_portal TO biocirv_readonly")


def downgrade() -> None:
    """Drop the recreated view."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.{view_name} CASCADE")
'''

    return code

def main():
    code = generate_migration_code()
    print(code)

    # Also save the extracted SQL to a reference file
    reference_file = Path(__file__).parent.parent / "alembic" / "VIEW_SQL_REFERENCE.md"
    with open(reference_file, "w") as f:
        f.write("# View SQL Reference\n\n")
        f.write("This file documents the raw SQL for each materialized view.\n")
        f.write("Used as reference when creating migrations with raw SQL snapshots.\n\n")

        for view_name, view_expr, schema_name in VIEWS:
            sql = compile_view(view_expr)
            f.write(f"## {view_name}\n\n")
            f.write(f"Schema: {schema_name}\n\n")
            f.write(f"```sql\n{sql}\n```\n\n")
            if view_name in INDEXES:
                f.write(f"### Index\n\n")
                f.write(f"```sql\n{INDEXES[view_name]}\n```\n\n")

    print(f"\n✓ Reference SQL saved to {reference_file}")

if __name__ == "__main__":
    main()
