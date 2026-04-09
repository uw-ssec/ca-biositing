#!/usr/bin/env python3
"""
Generate migration files for all remaining materialized views.

This script creates individual migration files for each view, following the
raw SQL snapshot pattern documented in alembic/AGENTS.md.

Usage:
    pixi run python scripts/generate_view_migrations.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Import all views
from ca_biositing.datamodels.data_portal_views import (
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
    {
        "name": "mv_biomass_availability",
        "expr": mv_biomass_availability,
        "schema": "data_portal.mv_biomass_availability",
        "revision": "9e8f7a6b5c4f",
        "down_revision": "9e8f7a6b5c4e",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_availability_id ON data_portal.mv_biomass_availability (resource_id)",
    },
    {
        "name": "mv_biomass_composition",
        "expr": mv_biomass_composition,
        "schema": "data_portal.mv_biomass_composition",
        "revision": "9e8f7a6b5c50",
        "down_revision": "9e8f7a6b5c4f",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)",
    },
    {
        "name": "mv_biomass_county_production",
        "expr": mv_biomass_county_production,
        "schema": "data_portal.mv_biomass_county_production",
        "revision": "9e8f7a6b5c51",
        "down_revision": "9e8f7a6b5c50",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_county_production_id ON data_portal.mv_biomass_county_production (id)",
    },
    {
        "name": "mv_biomass_sample_stats",
        "expr": mv_biomass_sample_stats,
        "schema": "data_portal.mv_biomass_sample_stats",
        "revision": "9e8f7a6b5c52",
        "down_revision": "9e8f7a6b5c51",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_id ON data_portal.mv_biomass_sample_stats (id)",
    },
    {
        "name": "mv_biomass_fermentation",
        "expr": mv_biomass_fermentation,
        "schema": "data_portal.mv_biomass_fermentation",
        "revision": "9e8f7a6b5c53",
        "down_revision": "9e8f7a6b5c52",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)",
    },
    {
        "name": "mv_biomass_gasification",
        "expr": mv_biomass_gasification,
        "schema": "data_portal.mv_biomass_gasification",
        "revision": "9e8f7a6b5c54",
        "down_revision": "9e8f7a6b5c53",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)",
    },
    {
        "name": "mv_biomass_pricing",
        "expr": mv_biomass_pricing,
        "schema": "data_portal.mv_biomass_pricing",
        "revision": "9e8f7a6b5c55",
        "down_revision": "9e8f7a6b5c54",
        "index": "CREATE UNIQUE INDEX idx_mv_biomass_pricing_id ON data_portal.mv_biomass_pricing (id)",
    },
    {
        "name": "mv_usda_county_production",
        "expr": mv_usda_county_production,
        "schema": "data_portal.mv_usda_county_production",
        "revision": "9e8f7a6b5c56",
        "down_revision": "9e8f7a6b5c55",
        "index": "CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)",
    },
]


def compile_view(select_expr):
    """Compile SQLAlchemy select() to PostgreSQL SQL."""
    compiled = select_expr.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    return str(compiled)


def generate_migration_content(view_config):
    """Generate migration file content for a single view."""
    view_name = view_config["name"]
    schema_name = view_config["schema"]
    revision = view_config["revision"]
    down_revision = view_config["down_revision"]
    index_sql = view_config["index"]

    # Compile SQL
    sql = compile_view(view_config["expr"])

    # Generate migration file
    content = f'''"""Recreate {view_name} with raw SQL snapshot.

Revision ID: {revision}
Revises: {down_revision}
Create Date: {datetime.now().isoformat()}

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '{revision}'
down_revision = '{down_revision}'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Recreate {view_name} with immutable SQL snapshot."""

    # Drop existing view if present
    op.execute("DROP MATERIALIZED VIEW IF EXISTS {schema_name} CASCADE")

    # Create view with immutable SQL snapshot
    # This SQL was compiled from SQLAlchemy at migration-creation time
    # and is frozen here for all future replays
    op.execute("""
        CREATE MATERIALIZED VIEW {schema_name} AS
        {sql}
    """)

    # Create index for performance
    op.execute("""
        {index_sql}
    """)

    # Grant schema access to readonly role
    op.execute("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly")
    op.execute("GRANT SELECT ON ALL MATERIALIZED VIEWS IN SCHEMA data_portal TO biocirv_readonly")


def downgrade() -> None:
    """Drop the recreated view."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS {schema_name} CASCADE")
'''

    return content


def main():
    alembic_versions_dir = Path(__file__).parent.parent / "alembic" / "versions"

    print("Generating migration files for remaining 8 views...\n")

    for view_config in VIEWS:
        view_name = view_config["name"]
        revision = view_config["revision"]

        # Generate filename
        filename = f"{revision}_recreate_{view_name}_with_raw_sql.py"
        filepath = alembic_versions_dir / filename

        # Generate content
        content = generate_migration_content(view_config)

        # Write file
        with open(filepath, "w") as f:
            f.write(content)

        print(f"✓ Created: {filename}")

    print(f"\n✨ Generated {len(VIEWS)} migration files in {alembic_versions_dir}")
    print("\nNext steps:")
    print("1. Review the generated migration files")
    print("2. Run: pixi run migrate")
    print("3. Verify views were created: pixi run access-db -c 'SELECT * FROM data_portal.mv_biomass_availability LIMIT 1;'")


if __name__ == "__main__":
    main()
