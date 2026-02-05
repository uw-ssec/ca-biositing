#!/usr/bin/env python3
"""
Test script to check what commodities are available in our target counties
via direct USDA NASS API queries.
"""

import os
import sys
import pandas as pd

# Add the pipeline utils to the path
sys.path.append('src/ca_biositing/pipeline/ca_biositing/pipeline/utils')

try:
    from usda_nass_to_pandas import usda_nass_to_df
except ImportError:
    print("Could not import usda_nass_to_pandas. Make sure you're running from the project root.")
    sys.exit(1)

# Configuration
USDA_API_KEY = os.getenv("USDA_NASS_API_KEY", "")
STATE = "CA"
PRIORITY_COUNTIES = ["077", "099", "047"]  # San Joaquin, Stanislaus, Merced

if not USDA_API_KEY:
    print("ERROR: USDA_NASS_API_KEY environment variable not set")
    sys.exit(1)

def test_county_commodities(county_code):
    """Query what commodities are available for a specific county"""
    print(f"\n=== Testing County {county_code} ===")

    # Query ALL commodities for this county (no commodity filter)
    df = usda_nass_to_df(
        api_key=USDA_API_KEY,
        state=STATE,
        county_code=county_code,
        commodity_ids=None,  # No filter - get all commodities
        commodity=None       # No filter - get all commodities
    )

    if df is not None and not df.empty:
        print(f"✓ Got {len(df)} total records for county {county_code}")

        # Show unique commodities
        if 'commodity' in df.columns:
            unique_commodities = sorted(df['commodity'].unique())
            print(f"✓ Found {len(unique_commodities)} unique commodities:")
            for i, commodity in enumerate(unique_commodities, 1):
                print(f"  {i:2d}. {commodity}")
        elif 'commodity_desc' in df.columns:
            unique_commodities = sorted(df['commodity_desc'].unique())
            print(f"✓ Found {len(unique_commodities)} unique commodities:")
            for i, commodity in enumerate(unique_commodities, 1):
                print(f"  {i:2d}. {commodity}")
        else:
            print("Columns in response:", df.columns.tolist())
            print(df.head())

        return unique_commodities
    else:
        print(f"✗ No data returned for county {county_code}")
        return []

def main():
    print("USDA NASS API Commodity Discovery")
    print("=" * 50)

    all_commodities = set()

    # Test each priority county
    for county_code in PRIORITY_COUNTIES:
        try:
            commodities = test_county_commodities(county_code)
            all_commodities.update(commodities)
        except Exception as e:
            print(f"Error testing county {county_code}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n=== SUMMARY ===")
    print(f"Total unique commodities across all 3 counties: {len(all_commodities)}")

    # Show our mapped commodities vs what's available
    our_commodities = [
        'ALL GRAPES', 'ALMONDS', 'CORN  ALL', 'CORN  FOR SILAGE', 'COTTON  UPLAND',
        'CUCUMBERS', 'HAY  ALFALFA (DRY)', 'OLIVES', 'PEACHES', 'PISTACHIO NUTS',
        'POTATOES  ALL', 'RICE  ALL', 'SWEETPOTATOES', 'TOMATOES',
        'TOMATOES FOR PROCESSING', 'WALNUTS (ENGLISH)', 'WHEAT'
    ]

    print(f"\nOur mapped commodities ({len(our_commodities)}):")
    for commodity in our_commodities:
        available = commodity in all_commodities
        status = "✓" if available else "✗"
        print(f"  {status} {commodity}")

    print(f"\nAvailable commodities we're NOT querying:")
    missing = all_commodities - set(our_commodities)
    for commodity in sorted(missing):
        print(f"  + {commodity}")

if __name__ == "__main__":
    main()
