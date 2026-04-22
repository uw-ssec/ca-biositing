#!/usr/bin/env python3
"""
Compile all data portal views to SQL for embedding in Alembic migration.
This script generates immutable SQL strings for the consolidated migration.
"""
import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Must set PROJ_LIB before importing geospatial libraries
import os
import pyproj
os.environ['PROJ_LIB'] = pyproj.datadir.get_data_dir()

from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql

# Import all view definitions
from ca_biositing.datamodels.ca_biositing.datamodels.data_portal_views import (
    mv_biomass_search,
    mv_biomass_availability,
    mv_biomass_composition,
    mv_biomass_county_production,
    mv_biomass_end_uses,
    mv_biomass_fermentation,
    mv_biomass_gasification,
    mv_biomass_pricing,
    mv_biomass_sample_stats,
    mv_usda_county_production,
    mv_billion_ton_county_production,
)

# List of all views to compile in order
VIEWS_TO_COMPILE = [
    ("mv_biomass_search", mv_biomass_search.mv_biomass_search),
    ("mv_biomass_availability", mv_biomass_availability.mv_biomass_availability),
    ("mv_biomass_composition", mv_biomass_composition.mv_biomass_composition),
    ("mv_biomass_county_production", mv_biomass_county_production.mv_biomass_county_production),
    ("mv_biomass_end_uses", mv_biomass_end_uses.mv_biomass_end_uses),
    ("mv_biomass_fermentation", mv_biomass_fermentation.mv_biomass_fermentation),
    ("mv_biomass_gasification", mv_biomass_gasification.mv_biomass_gasification),
    ("mv_biomass_pricing", mv_biomass_pricing.mv_biomass_pricing),
    ("mv_biomass_sample_stats", mv_biomass_sample_stats.mv_biomass_sample_stats),
    ("mv_usda_county_production", mv_usda_county_production.mv_usda_county_production),
    ("mv_billion_ton_county_production", mv_billion_ton_county_production.mv_billion_ton_county_production),
]

def compile_view_to_sql(view_name: str, select_stmt) -> str:
    """Compile a SQLAlchemy select statement to PostgreSQL SQL."""
    # Create a dummy engine for compilation
    engine = create_engine("postgresql://dummy", strategy='mock', executor=lambda sql, *_: None)

    # Compile to PostgreSQL dialect
    compiled = select_stmt.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )

    sql_str = str(compiled)
    return sql_str

def main():
    print("=" * 80)
    print("COMPILING ALL DATA PORTAL VIEWS TO SQL")
    print("=" * 80)
    print()

    for view_name, select_stmt in VIEWS_TO_COMPILE:
        print(f"\n{'='*80}")
        print(f"VIEW: {view_name}")
        print(f"{'='*80}")
        try:
            sql = compile_view_to_sql(view_name, select_stmt)
            print(sql)
        except Exception as e:
            print(f"ERROR compiling {view_name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
