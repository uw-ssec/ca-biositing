#!/usr/bin/env python3
"""
Compile materialized view definitions from Python to PostgreSQL SQL.

This script imports the updated view definitions and compiles them to SQL
using SQLAlchemy's PostgreSQL dialect with literal_binds to expand parameters.

Usage:
    pixi run python scripts/compile_views.py
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sqlalchemy import text
from sqlalchemy.dialects import postgresql

# Import the view modules
from ca_biositing.datamodels.data_portal_views.mv_biomass_composition import mv_biomass_composition
from ca_biositing.datamodels.data_portal_views.mv_biomass_gasification import mv_biomass_gasification
from ca_biositing.datamodels.data_portal_views.mv_biomass_fermentation import mv_biomass_fermentation
from ca_biositing.datamodels.data_portal_views.mv_biomass_sample_stats import mv_biomass_sample_stats

def compile_view(view_select, view_name):
    """Compile a SQLAlchemy select statement to PostgreSQL SQL."""
    try:
        # Compile with PostgreSQL dialect and literal_binds
        compiled = view_select.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
        sql = str(compiled)
        print(f"\n{'='*80}")
        print(f"View: {view_name}")
        print(f"{'='*80}")
        print(sql)
        print()
        return sql
    except Exception as e:
        print(f"Error compiling {view_name}: {e}")
        return None

def main():
    """Compile all updated views to SQL."""
    print("Compiling materialized view definitions to PostgreSQL SQL...")
    print("(After QC filtering changes: qc_pass != 'fail')")

    compiled_views = {}

    # Compile each view
    views = [
        (mv_biomass_composition, "mv_biomass_composition"),
        (mv_biomass_gasification, "mv_biomass_gasification"),
        (mv_biomass_fermentation, "mv_biomass_fermentation"),
        (mv_biomass_sample_stats, "mv_biomass_sample_stats"),
    ]

    for view_select, view_name in views:
        sql = compile_view(view_select, view_name)
        if sql:
            compiled_views[view_name] = sql

    # Save compiled SQL to file
    output_file = "exports/compiled_views.sql"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write("-- Compiled materialized view definitions\n")
        f.write("-- Generated from Python view modules after QC filtering changes\n")
        f.write("-- QC Filter: qc_pass != 'fail' (exclude only records marked as failed)\n")
        f.write("-- Date: 2026-04-07\n\n")

        for view_name, sql in compiled_views.items():
            f.write(f"-- View: {view_name}\n")
            f.write(f"{sql};\n\n")

    print(f"\n✓ Compiled SQL saved to: {output_file}")
    print(f"✓ Total views compiled: {len(compiled_views)}")

    return len(compiled_views)

if __name__ == "__main__":
    count = main()
    sys.exit(0 if count > 0 else 1)
