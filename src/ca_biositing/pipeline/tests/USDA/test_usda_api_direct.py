#!/usr/bin/env python3
"""Test subset of individual USDA API calls to see what's being returned"""

import os
import requests
import json

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading if dotenv not available
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

API_KEY = os.getenv("USDA_NASS_API_KEY", "")

def test_commodity_query(commodity_name, county_code="077"):
    """Test a single commodity query to see what the API returns"""
    url = "https://quickstats.nass.usda.gov/api/api_GET"

    params = {
        "key": API_KEY,
        "state_alpha": "CA",
        "county_code": county_code,
        "commodity_desc": commodity_name,
        "agg_level_desc": "COUNTY",
        "domain_desc": "TOTAL",
        "format": "JSON"
    }

    print(f"\n🔍 Testing commodity: '{commodity_name}' for county {county_code}")
    print(f"Query URL: {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and "error" in data:
            print(f"❌ API Error: {data['error']}")
            return []

        # Extract actual data
        if isinstance(data, dict) and "data" in data:
            actual_data = data["data"]
        elif isinstance(data, list):
            actual_data = data
        else:
            actual_data = []

        print(f"✅ Got {len(actual_data)} records")

        if actual_data:
            # Show first record structure
            print(f"Sample record keys: {list(actual_data[0].keys())}")

            # Show unique commodity info from results
            commodities = set()
            for record in actual_data[:10]:  # Just first 10
                commodities.add(record.get('commodity_desc', 'N/A'))

            print(f"Commodity descriptions returned: {list(commodities)}")

        return actual_data

    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

def main():
    if not API_KEY:
        print("❌ USDA_NASS_API_KEY not set!")
        return

    # Test a few of our mapped commodities
    test_commodities = [
        "WHEAT",        # Should be simple
        "ALMONDS",      # Should work
        "PISTACHIOS",   # Might have issues
        "HAY",          # Might be too generic
        "GRAPES"        # Should work
    ]

    for commodity in test_commodities:
        results = test_commodity_query(commodity, "077")  # San Joaquin County

if __name__ == "__main__":
    main()
