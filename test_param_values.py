#!/usr/bin/env python3
"""
Test to discover ALL possible commodity values from USDA NASS API
using the get_param_values endpoint.
"""

import os
import sys
import requests
import pandas as pd

# Test the get_param_values endpoint to get all commodity options
def test_param_values_endpoint():
    """Test if USDA API has a get_param_values endpoint"""
    api_key = os.getenv('USDA_NASS_API_KEY', '')
    if not api_key:
        print("No API key available")
        return None

    base_url = "https://quickstats.nass.usda.gov/api"

    # Try the get_param_values endpoint (based on R package documentation)
    url = f"{base_url}/get_param_values"
    params = {
        "key": api_key,
        "param": "commodity_desc"  # Get all possible commodity descriptions
    }

    print("Testing get_param_values endpoint...")
    print(f"URL: {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Success! Response preview:")
            print(f"Type: {type(data)}")

            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")

                # Check for commodity_desc key
                if 'commodity_desc' in data:
                    commodities = data['commodity_desc']
                    print(f"Commodity data type: {type(commodities)}")
                    print(f"Commodity count: {len(commodities) if isinstance(commodities, list) else 'not a list'}")
                    if isinstance(commodities, list) and len(commodities) > 0:
                        print(f"Sample commodities: {commodities[:10]}")

                elif 'data' in data:
                    print(f"Data length: {len(data['data'])}")
                    print(f"Sample values: {data['data'][:10]}")
                elif isinstance(data, list):
                    print(f"List length: {len(data)}")
                    print(f"Sample values: {data[:10]}")
                else:
                    print("Raw response:", data)
            return data
        else:
            print(f"Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("USDA API Parameter Discovery Test")
    print("=" * 50)

    # Test get_param_values endpoint
    commodity_data = test_param_values_endpoint()

    if commodity_data:
        print("\n=== ANALYSIS ===")

        # Extract commodity list
        commodities = None
        if isinstance(commodity_data, dict) and 'commodity_desc' in commodity_data:
            commodities = commodity_data['commodity_desc']
        elif isinstance(commodity_data, dict) and 'data' in commodity_data:
            commodities = commodity_data['data']
        elif isinstance(commodity_data, list):
            commodities = commodity_data

        if commodities:
            print(f"Found {len(commodities)} total commodities")
            print("\nAll available commodities:")
            for i, commodity in enumerate(commodities, 1):
                print(f"  {i:3d}. {commodity}")

            # Compare with our current mappings
            our_commodities = [
                'ALL GRAPES', 'ALMONDS', 'CORN  ALL', 'CORN  FOR SILAGE',
                'COTTON  UPLAND', 'CUCUMBERS', 'HAY  ALFALFA (DRY)', 'OLIVES',
                'PEACHES', 'PISTACHIO NUTS', 'POTATOES  ALL', 'RICE  ALL',
                'SWEETPOTATOES', 'TOMATOES', 'TOMATOES FOR PROCESSING',
                'WALNUTS (ENGLISH)', 'WHEAT'
            ]

            print(f"\n=== COMMODITY COMPARISON ===")
            print("Our current mappings vs. official API values:")

            commodity_set = set(commodities)
            for commodity in our_commodities:
                if commodity in commodity_set:
                    print(f"  ✓ {commodity}")
                else:
                    print(f"  ✗ {commodity}")

            print(f"\nCommodities we could map to but aren't:")
            unmapped = commodity_set - set(our_commodities)
            for commodity in sorted(unmapped):
                print(f"  + {commodity}")

        else:
            print("Could not extract commodity list from response")
    else:
        print("Could not get commodity parameter values from API")

if __name__ == "__main__":
    main()
