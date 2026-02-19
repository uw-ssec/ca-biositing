#!/usr/bin/env python3
"""
Test USDA API availability for our specific commodities and counties

NOTE: This script queries USDA NASS API for raw commodity data availability.
Results are NOT filtered for specific parameters (like AREA BEARING vs AREA HARVESTED)
or units of interest. This is a broad availability check only.
"""

import requests
import time
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading if dotenv not available - look in project root
    import os
    current_dir = os.path.dirname(__file__)
    # Navigate up to project root: tests/USDA -> pipeline -> ca_biositing -> src -> root
    env_path = os.path.join(current_dir, '..', '..', '..', '..', '..', '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

API_KEY = os.getenv('USDA_NASS_API_KEY', 'A95E83AA-D37A-37D7-8365-3C77DD57CE34')
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET"

# Our target counties (NASS codes)
COUNTIES = ["077", "099", "047"]  # San Joaquin, Stanislaus, Merced

# All 16 commodities mapped in our ETL pipeline
COMMODITIES = [
    "WHEAT", "TOMATOES", "CUCUMBERS",  # Working commodities (codes 3, 4, 222)
    "ALMONDS", "GRAPES", "PISTACHIOS", "WALNUTS",  # Tree nuts and grapes
    "PEACHES", "OLIVES",  # Other fruit commodities
    "CORN", "COTTON", "HAY",  # Field crops
    "RICE", "OATS", "BARLEY", "SILAGE"  # Additional crops
]

def test_commodity_in_county(commodity, county_code):
    """Test if a commodity has data in a specific county"""
    params = {
        "key": API_KEY,
        "state_alpha": "CA",
        "county_code": county_code,
        "commodity_desc": commodity,
        "agg_level_desc": "COUNTY",
        "domain_desc": "TOTAL",
        "format": "JSON"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and "error" in data:
            return 0, data["error"]

        # Extract actual data
        if isinstance(data, dict) and "data" in data:
            actual_data = data["data"]
        elif isinstance(data, list):
            actual_data = data
        else:
            actual_data = []

        return len(actual_data), None

    except Exception as e:
        return 0, str(e)

def main():
    print(f"🔍 Testing USDA API data availability for {len(COMMODITIES)} commodities in {len(COUNTIES)} counties...")
    print(f"Counties: San Joaquin (077), Stanislaus (099), Merced (047)")
    print("\n⚠️  NOTE: Results show raw data availability, NOT filtered for specific")
    print("   parameters (AREA BEARING vs AREA HARVESTED) or units of interest.")
    print("   This is a broad availability check only.\n")

    results = {}

    for commodity in COMMODITIES:
        print(f"Testing commodity: {commodity}")
        commodity_results = {}

        for county in COUNTIES:
            records, error = test_commodity_in_county(commodity, county)
            commodity_results[county] = records

            if error:
                print(f"  County {county}: ERROR - {error}")
            else:
                print(f"  County {county}: {records} records")

            time.sleep(0.5)  # Rate limiting

        results[commodity] = commodity_results
        total_records = sum(commodity_results.values())
        print(f"  TOTAL for {commodity}: {total_records} records across all counties")
        print()

    print("📊 SUMMARY:")
    for commodity, county_results in results.items():
        total = sum(county_results.values())
        if total > 0:
            print(f"✅ {commodity}: {total} records")
        else:
            print(f"❌ {commodity}: NO DATA")

if __name__ == "__main__":
    main()
