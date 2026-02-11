#!/usr/bin/env python3
"""
Test script to check what data is available for missing commodities in USDA API
"""

import requests
import os
from typing import List

# Configuration
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET"
API_KEY = os.getenv('USDA_NASS_API_KEY', 'YOUR_API_KEY_HERE')
STATE = "CA"
YEAR = "2019"  # 2017 and 2012 are also used
COUNTY_CODES = ["077", "099", "047"]  # San Joaquin, Stanislaus, Merced

MISSING_COMMODITIES = [
    "ALMONDS", "GRAPES", "OLIVES", "PEACHES",
    "PISTACHIOS", "SILAGE", "WALNUTS"
]

def check_commodity_availability(commodity: str) -> dict:
    """Check what data is available for a specific commodity"""
    print(f"\n🔍 Checking {commodity}...")

    results = {}

    for county_code in COUNTY_CODES:
        params = {
            "key": API_KEY,
            "state_alpha": STATE,
            "year": YEAR,
            "county_code": county_code,
            "commodity_desc": commodity,
            "format": "JSON",
            "domain_desc": "TOTAL"
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and data['data']:
                count = len(data['data'])
                print(f"  ✅ County {county_code}: {count} records")

                # Show what statistics are available
                stats = set(record.get('statisticcat_desc', 'N/A') for record in data['data'])
                print(f"     Statistics: {', '.join(sorted(stats))}")

                results[county_code] = {
                    'count': count,
                    'statistics': list(stats),
                    'sample_record': data['data'][0] if data['data'] else None
                }
            else:
                print(f"  ❌ County {county_code}: No data")
                results[county_code] = {'count': 0, 'statistics': [], 'sample_record': None}

        except Exception as e:
            print(f"  🚫 County {county_code}: Error - {e}")
            results[county_code] = {'error': str(e)}

    return results

def main():
    print("🌾 USDA API Availability Check for Missing Commodities")
    print("=" * 60)
    print(f"State: {STATE}")
    print(f"Year: {YEAR}")
    print(f"Counties: {', '.join(COUNTY_CODES)}")
    print(f"API Key: {'✅ Set' if API_KEY != 'YOUR_API_KEY_HERE' else '❌ Missing'}")

    if API_KEY == 'YOUR_API_KEY_HERE':
        print("\n❌ USDA_NASS_API_KEY environment variable not set!")
        print("   Get one from: https://quickstats.nass.usda.gov/api")
        return

    all_results = {}

    for commodity in MISSING_COMMODITIES:
        all_results[commodity] = check_commodity_availability(commodity)

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    for commodity, results in all_results.items():
        total_records = sum(r.get('count', 0) for r in results.values() if 'error' not in r)
        total_counties = sum(1 for r in results.values() if r.get('count', 0) > 0)

        if total_records > 0:
            print(f"✅ {commodity}: {total_records} records across {total_counties} counties")
        else:
            print(f"❌ {commodity}: No data found")

    print("\n💡 RECOMMENDATIONS:")
    print("- Check if these commodities use different names in USDA API")
    print("- Try different years (2017, 2012)")
    print("- Check if specific statisticcat_desc values are needed")
    print("- Verify usda_code values in commodity_mappings_corrected.csv")

if __name__ == "__main__":
    main()
