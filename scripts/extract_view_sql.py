#!/usr/bin/env python3
"""
Extract raw SQL from SQLAlchemy view definitions.

This script compiles each materialized view to raw SQL for embedding in migrations.
Ensures migrations are immutable and not affected by future schema changes.

Usage:
    pixi run python scripts/extract_view_sql.py
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

VIEWS = {
    "mv_biomass_search": (mv_biomass_search, "data_portal.mv_biomass_search"),
    "mv_biomass_availability": (mv_biomass_availability, "data_portal.mv_biomass_availability"),
    "mv_biomass_composition": (mv_biomass_composition, "data_portal.mv_biomass_composition"),
    "mv_biomass_county_production": (mv_biomass_county_production, "data_portal.mv_biomass_county_production"),
    "mv_biomass_sample_stats": (mv_biomass_sample_stats, "data_portal.mv_biomass_sample_stats"),
    "mv_biomass_fermentation": (mv_biomass_fermentation, "data_portal.mv_biomass_fermentation"),
    "mv_biomass_gasification": (mv_biomass_gasification, "data_portal.mv_biomass_gasification"),
    "mv_biomass_pricing": (mv_biomass_pricing, "data_portal.mv_biomass_pricing"),
    "mv_usda_county_production": (mv_usda_county_production, "data_portal.mv_usda_county_production"),
}

def compile_view(select_expr):
    """Compile SQLAlchemy select() to PostgreSQL SQL."""
    compiled = select_expr.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    return str(compiled)

def main():
    print("=" * 80)
    print("VIEW SQL EXTRACTION")
    print("=" * 80)
    print()

    for view_name, (view_expr, schema_name) in VIEWS.items():
        print(f"\n{'=' * 80}")
        print(f"View: {view_name}")
        print(f"Schema: {schema_name}")
        print(f"{'=' * 80}\n")

        try:
            sql = compile_view(view_expr)
            print(sql)
            print()
        except Exception as e:
            print(f"ERROR compiling {view_name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
