#!/usr/bin/env python3
"""
Test script to show what happens in the transform step before and after our fix
"""

import pandas as pd
import os
from sqlalchemy import create_engine, text

def show_transform_issue():
    """Demonstrate the transform step issue and fix"""

    print("🔍 USDA TRANSFORM STEP ANALYSIS")
    print("=" * 50)

    # Connect to database
    db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db')
    engine = create_engine(db_url, echo=False)

    # 1. Show what the API returns (simulated)
    print("\n1. 📥 WHAT THE USDA API RETURNS:")
    print("Sample data from USDA API for different commodities:")

    # This simulates what the USDA API returns based on our api_names
    api_data = {
        'commodity_desc': ['WHEAT', 'ALMONDS', 'HAY', 'PISTACHIOS', 'GRAPES'],
        'short_desc': ['WHEAT - AREA HARVESTED', 'ALMONDS - PRODUCTION', 'HAY - AREA HARVESTED', 'PISTACHIOS - YIELD', 'GRAPES - PRODUCTION'],
        'value': [1000, 2000, 1500, 800, 3000],
        'state_alpha': ['CA', 'CA', 'CA', 'CA', 'CA'],
        'county_code': ['077', '077', '077', '077', '077']
    }

    api_df = pd.DataFrame(api_data)
    print(api_df.to_string(index=False))

    # 2. Show what's in the database (OLD way - using 'name' field)
    print("\n\n2. 🗃️ OLD COMMODITY MAP (using usda_commodity.name):")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, UPPER(name) as commodity_name
            FROM usda_commodity
            ORDER BY id
        """))
        old_commodity_map = {row[1]: row[0] for row in result.fetchall()}

    print("Commodity map built from 'name' field:")
    for name, code in list(old_commodity_map.items())[:5]:
        print(f"  '{name}' → {code}")

    # 3. Show what happens when we try to map (OLD way)
    print("\n\n3. ❌ OLD TRANSFORM RESULT:")
    print("Mapping API commodity names using OLD commodity map:")

    api_df['commodity_upper'] = api_df['commodity_desc'].str.upper()
    api_df['commodity_code_old'] = api_df['commodity_upper'].map(old_commodity_map)

    transform_result_old = api_df[['commodity_desc', 'commodity_upper', 'commodity_code_old']].copy()
    print(transform_result_old.to_string(index=False))

    success_count_old = transform_result_old['commodity_code_old'].notna().sum()
    print(f"\n🔢 Successfully mapped: {success_count_old}/{len(transform_result_old)} commodities")

    # 4. Show NEW way (using api_name field)
    print("\n\n4. 🗃️ NEW COMMODITY MAP (using usda_commodity.api_name):")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, UPPER(api_name) as commodity_name
            FROM usda_commodity
            WHERE api_name IS NOT NULL
            ORDER BY id
        """))
        new_commodity_map = {row[1]: row[0] for row in result.fetchall()}

    print("Commodity map built from 'api_name' field:")
    for name, code in list(new_commodity_map.items())[:5]:
        print(f"  '{name}' → {code}")

    # 5. Show what happens when we map (NEW way)
    print("\n\n5. ✅ NEW TRANSFORM RESULT:")
    print("Mapping API commodity names using NEW commodity map:")

    api_df['commodity_code_new'] = api_df['commodity_upper'].map(new_commodity_map)

    transform_result_new = api_df[['commodity_desc', 'commodity_upper', 'commodity_code_new']].copy()
    print(transform_result_new.to_string(index=False))

    success_count_new = transform_result_new['commodity_code_new'].notna().sum()
    print(f"\n🔢 Successfully mapped: {success_count_new}/{len(transform_result_new)} commodities")

    # 6. Summary
    print("\n\n📊 SUMMARY:")
    print(f"OLD method (using 'name'): {success_count_old}/{len(transform_result_old)} commodities mapped")
    print(f"NEW method (using 'api_name'): {success_count_new}/{len(transform_result_new)} commodities mapped")
    print(f"Improvement: +{success_count_new - success_count_old} commodities")

    print("\n🔧 THE FIX:")
    print("Changed line 151 in transform step:")
    print("OLD: commodity_map built from usda_commodity.name")
    print("NEW: commodity_map built from usda_commodity.api_name")
    print("\nThis ensures the transform step can map the commodity names")
    print("that come back from the USDA API to the correct commodity codes.")

if __name__ == "__main__":
    show_transform_issue()
