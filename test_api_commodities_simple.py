#!/usr/bin/env python3

import os
import sys
import pandas as pd

# Test 1: Check environment
print("=== Environment Test ===")
print("USDA_NASS_API_KEY set:", bool(os.getenv('USDA_NASS_API_KEY')))
print("Working directory:", os.getcwd())
print("Python path:", sys.path[:3])

# Test 2: Try to import the utility
sys.path.insert(0, '/app/src/ca_biositing/pipeline/ca_biositing/pipeline/utils')
sys.path.insert(0, '/app/src/ca_biositing/pipeline')
print("\n=== Import Test ===")
try:
    from ca_biositing.pipeline.utils.usda_nass_to_pandas import usda_nass_to_df
    print("✓ Successfully imported usda_nass_to_pandas")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 3: API call for ALL commodities in one county
print("\n=== API Test ===")
api_key = os.getenv('USDA_NASS_API_KEY')
if not api_key:
    print("✗ No API key available")
    sys.exit(1)

print("Testing Merced County (047) - ALL commodities...")
try:
    df = usda_nass_to_df(
        api_key=api_key,
        state='CA',
        county_code='047',
        # No commodity filter - should return ALL available commodities
    )

    if df is not None and not df.empty:
        print(f"✓ Success! Got {len(df)} total records")
        print("Columns available:", list(df.columns))

        # Find the commodity column
        commodity_col = None
        for col in ['commodity_desc', 'commodity']:
            if col in df.columns:
                commodity_col = col
                break

        if commodity_col:
            commodities = sorted(df[commodity_col].unique())
            print(f"\n✓ Found {len(commodities)} unique commodities:")
            for i, commodity in enumerate(commodities, 1):
                print(f"  {i:2d}. {commodity}")

            # Check our mapped commodities
            our_commodities = [
                'ALL GRAPES', 'ALMONDS', 'CORN  ALL', 'CORN  FOR SILAGE',
                'COTTON  UPLAND', 'CUCUMBERS', 'HAY  ALFALFA (DRY)', 'OLIVES',
                'PEACHES', 'PISTACHIO NUTS', 'POTATOES  ALL', 'RICE  ALL',
                'SWEETPOTATOES', 'TOMATOES', 'TOMATOES FOR PROCESSING',
                'WALNUTS (ENGLISH)', 'WHEAT'
            ]

            print(f"\n=== Commodity Matching Analysis ===")
            print("Our mapped commodities vs. what's available in API:")

            available_set = set(commodities)
            for commodity in our_commodities:
                if commodity in available_set:
                    print(f"  ✓ {commodity}")
                else:
                    print(f"  ✗ {commodity}")

        else:
            print("No commodity column found. Sample data:")
            print(df.head())

    else:
        print("✗ No data returned from API")

except Exception as e:
    print(f"✗ API call failed: {e}")
    import traceback
    traceback.print_exc()
