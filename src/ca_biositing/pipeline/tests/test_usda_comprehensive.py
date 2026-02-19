#!/usr/bin/env python3
"""
COMPREHENSIVE USDA ETL TESTING AND DIAGNOSTICS

This script consolidates all USDA testing functionality into one robust tool.
It covers API connectivity, database state verification, commodity mapping checks,
and ETL pipeline validation. Use this as the single source of truth for debugging
USDA data issues.

USAGE:
  python comprehensive_usda_test.py --api          # Test API connectivity only
  python comprehensive_usda_test.py --database    # Check database state only
  python comprehensive_usda_test.py --mapping     # Check commodity mappings only
  python comprehensive_usda_test.py --all         # Run all tests (default)
"""

import os
import sys
import argparse
import requests
import pandas as pd
from typing import Dict, List, Optional
from sqlalchemy import create_engine, text
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv not available, try manual loading
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Configuration
API_KEY = os.getenv('USDA_NASS_API_KEY', '')
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET"
COUNTIES = ["077", "099", "047"]  # San Joaquin, Stanislaus, Merced
DATABASE_PORTS = [9090, 5432]  # Try containerized port first, then standard
STATE = "CA"
TIMEOUT = 30

def get_database_engine():
    """Get database connection with port fallback"""
    db_base_url = "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:{}/biocirv_db"

    for port in DATABASE_PORTS:
        try:
            engine = create_engine(db_base_url.format(port), echo=False)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"✅ Database connected on port {port}")
            return engine
        except Exception as e:
            print(f"❌ Port {port} failed: {e}")
            continue

    raise Exception(f"Could not connect to database on any port: {DATABASE_PORTS}")

class USDAAPITester:
    """Test USDA API connectivity and data availability"""

    def __init__(self):
        if not API_KEY:
            raise ValueError("USDA_NASS_API_KEY environment variable required")

    def test_api_connectivity(self) -> bool:
        """Test basic API connectivity with a small query"""
        try:
            # Use a smaller query to avoid 413 error - just one commodity
            params = {
                "key": API_KEY,
                "state_alpha": STATE,
                "commodity_desc": "CORN",
                "year": "2023",
                "county_code": "077",  # Just San Joaquin county
                "format": "JSON"
            }
            response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
            response.raise_for_status()

            # Handle empty responses that can't be parsed as JSON
            if not response.text.strip():
                print(f"⚠️ API returned empty response for connectivity test")
                return False

            try:
                data = response.json()
            except ValueError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"Response content: {response.text[:200]}")
                return False

            if 'data' in data and data['data']:
                print(f"✅ API connectivity successful - {len(data['data'])} records found")
                return True
            else:
                print(f"⚠️ API connected but no data returned: {data}")
                return False

        except Exception as e:
            print(f"❌ API connectivity failed: {e}")
            return False

    def test_commodity_availability(self, commodity: str, county: str) -> Dict:
        """Test specific commodity availability in a county"""
        params = {
            "key": API_KEY,
            "state_alpha": STATE,
            "county_code": county,
            "commodity_desc": commodity,
            "agg_level_desc": "COUNTY",
            "domain_desc": "TOTAL",
            "format": "JSON"
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
            response.raise_for_status()

            # Handle empty responses that can't be parsed as JSON
            if not response.text.strip():
                if commodity == "TOMATOES" and county == "077":
                    print(f"\n🔍 DEBUG - TOMATOES County 077 (Empty Response):")
                    print(f"   Request URL: {response.url}")
                    print(f"   Status Code: {response.status_code}")
                    print(f"   Response Length: {len(response.text)}")
                    print(f"   Response Headers: {dict(response.headers)}")
                return {
                    'status': 'ERROR',
                    'message': 'API returned empty response'
                }

            try:
                data = response.json()
            except ValueError as json_err:
                if commodity == "TOMATOES" and county == "077":
                    print(f"\n🔍 DEBUG - TOMATOES County 077 (JSON Error):")
                    print(f"   Request URL: {response.url}")
                    print(f"   Status Code: {response.status_code}")
                    print(f"   Response Length: {len(response.text)}")
                    print(f"   Response Headers: {dict(response.headers)}")
                    print(f"   Raw Response: {response.text[:500]}")
                return {
                    'status': 'ERROR',
                    'message': f'Failed to parse JSON: {json_err}. Response: {response.text[:100]}'
                }

            if 'data' in data and data['data']:
                return {
                    'status': 'SUCCESS',
                    'records': len(data['data']),
                    'years': sorted(set(r.get('year', 'N/A') for r in data['data']))
                }
            else:
                if commodity == "TOMATOES" and county == "077":
                    print(f"\n🔍 DEBUG - TOMATOES County 077 (No Data):")
                    print(f"   Request URL: {response.url}")
                    print(f"   Status Code: {response.status_code}")
                    print(f"   Response Length: {len(response.text)}")
                    print(f"   Response Headers: {dict(response.headers)}")
                    print(f"   Raw Response: {response.text[:500]}")
                return {
                    'status': 'NO_DATA',
                    'message': data.get('error', ['No data available'])[0] if data.get('error') else 'No records'
                }

        except Exception as e:
            return {
                'status': 'ERROR',
                'message': str(e)
            }

    def comprehensive_api_test(self, commodities: List[str]) -> Dict:
        """Run comprehensive API tests for all commodities and counties"""
        print(f"\n🔍 COMPREHENSIVE API TESTING")
        print("=" * 50)

        if not self.test_api_connectivity():
            return {'connectivity': False}

        results = {'connectivity': True, 'commodities': {}}

        for commodity in commodities:
            print(f"\nTesting {commodity}:")
            commodity_results = {}

            for county in COUNTIES:
                result = self.test_commodity_availability(commodity, county)
                status = result['status']

                if status == 'SUCCESS':
                    print(f"  County {county}: ✅ {result['records']} records, years: {result['years']}")
                elif status == 'NO_DATA':
                    print(f"  County {county}: ⚠️ No data - {result['message']}")
                else:
                    print(f"  County {county}: ❌ Error - {result['message']}")

                commodity_results[county] = result

            results['commodities'][commodity] = commodity_results

        return results

class DatabaseAnalyzer:
    """Analyze database state and commodity mappings"""

    def __init__(self):
        self.engine = get_database_engine()

    def check_commodity_table(self) -> Dict:
        """Check usda_commodity table contents"""
        with self.engine.connect() as conn:
            result = conn.execute(text('SELECT id, name, api_name FROM usda_commodity ORDER BY id'))
            commodities = {row[0]: {'name': row[1], 'api_name': row[2]} for row in result}

            return commodities

    def check_data_records(self) -> Dict:
        """Check census and survey record data"""
        with self.engine.connect() as conn:
            # Census records
            result = conn.execute(text('SELECT DISTINCT commodity_code FROM usda_census_record ORDER BY commodity_code'))
            census_codes = set(row[0] for row in result)

            # Survey records
            result = conn.execute(text('SELECT DISTINCT commodity_code FROM usda_survey_record ORDER BY commodity_code'))
            survey_codes = set(row[0] for row in result)

            return {
                'census_codes': census_codes,
                'survey_codes': survey_codes,
                'all_codes': census_codes.union(survey_codes)
            }

    def check_observations(self) -> Dict:
        """Check observation counts"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    record_type,
                    COUNT(*) as observation_count,
                    COUNT(DISTINCT record_id) as unique_records
                FROM observation
                WHERE record_type IN ('usda_census_record', 'usda_survey_record')
                GROUP BY record_type
            """))

            observations = {}
            for row in result:
                observations[row[0]] = {
                    'observations': row[1],
                    'unique_records': row[2]
                }

            return observations

    def check_etl_tracking(self) -> Dict:
        """Check ETL tracking tables (data_source, dataset, etc.)"""
        etl_counts = {}

        # Check data_source table
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM data_source"))
            etl_counts['data_source'] = result.scalar()

            # Check dataset table
            result = conn.execute(text("SELECT COUNT(*) FROM dataset"))
            etl_counts['dataset'] = result.scalar()

            # Check usda_census_record table
            result = conn.execute(text("SELECT COUNT(*) FROM usda_census_record"))
            etl_counts['usda_census_record'] = result.scalar()

            # Check usda_survey_record table
            result = conn.execute(text("SELECT COUNT(*) FROM usda_survey_record"))
            etl_counts['usda_survey_record'] = result.scalar()

        return etl_counts

    def check_parameters_units(self) -> Dict:
        """Check parameters and units likely added by USDA ETL"""
        with self.engine.connect() as conn:
            # Count total parameters
            result = conn.execute(text("SELECT COUNT(*) FROM parameter"))
            param_count = result.scalar()

            # Get parameters that look like USDA ones (common USDA statistics)
            usda_params = conn.execute(text("""
                SELECT name FROM parameter
                WHERE UPPER(name) IN (
                    'YIELD', 'PRODUCTION', 'AREA HARVESTED', 'AREA PLANTED',
                    'AREA BEARING', 'AREA NON-BEARING', 'OPERATIONS',
                    'PRICE RECEIVED', 'SALES', 'AREA IN PRODUCTION'
                )
                ORDER BY name
            """)).fetchall()

            # Count total units
            result = conn.execute(text("SELECT COUNT(*) FROM unit"))
            unit_count = result.scalar()

            # Get units that look like USDA ones
            usda_units = conn.execute(text("""
                SELECT name FROM unit
                WHERE UPPER(name) IN (
                    'BUSHELS', 'TONS', 'ACRES', 'DOLLARS', 'OPERATIONS',
                    'BU', 'LB', 'BALES', 'CWT', 'NUMBER', 'TONS / ACRE'
                )
                ORDER BY name
            """)).fetchall()

        return {
            'parameter_count': param_count,
            'recent_parameters': [row[0] for row in usda_params],
            'unit_count': unit_count,
            'recent_units': [row[0] for row in usda_units]
        }

    def comprehensive_database_analysis(self) -> Dict:
        """Run comprehensive database analysis"""
        print(f"\n🔍 COMPREHENSIVE DATABASE ANALYSIS")
        print("=" * 50)

        commodities = self.check_commodity_table()
        records = self.check_data_records()
        observations = self.check_observations()
        etl_tracking = self.check_etl_tracking()
        parameters_units = self.check_parameters_units()

        print(f'\n=== ETL TRACKING TABLES ===')
        for table, count in etl_tracking.items():
            print(f'{table}: {count} records')

        print(f'\n=== PARAMETERS AND UNITS ADDED ===')
        print(f"Parameters in database: {parameters_units['parameter_count']} total")
        if parameters_units['recent_parameters']:
            print("Recent parameters (likely from USDA ETL):")
            for param in parameters_units['recent_parameters'][:10]:  # Show first 10
                print(f"  - {param}")

        print(f"Units in database: {parameters_units['unit_count']} total")
        if parameters_units['recent_units']:
            print("Recent units (likely from USDA ETL):")
            for unit in parameters_units['recent_units'][:10]:  # Show first 10
                print(f"  - {unit}")

        print(f'\n=== USDA_COMMODITY TABLE ({len(commodities)} total) ===')
        for id, info in commodities.items():
            print(f'{id:3}: name="{info["name"]}" api_name="{info["api_name"]}"')

        print(f'\n=== DATA RECORDS ANALYSIS ===')
        print(f'Census records: {len(records["census_codes"])} unique commodity codes')
        print(f'Survey records: {len(records["survey_codes"])} unique commodity codes')
        print(f'Total unique: {len(records["all_codes"])} commodity codes')

        census_only = records["census_codes"] - records["survey_codes"]
        survey_only = records["survey_codes"] - records["census_codes"]
        both = records["census_codes"].intersection(records["survey_codes"])

        print(f'In both census and survey: {len(both)}')
        if census_only:
            # Get commodity names for census-only IDs
            census_only_details = []
            for commodity_id in sorted(census_only):
                if commodity_id in commodities:
                    name = commodities[commodity_id]['name']
                    census_only_details.append(f"{commodity_id}:{name}")
                else:
                    census_only_details.append(str(commodity_id))
            print(f'Census-only ({len(census_only)}): {census_only_details}')
        if survey_only:
            # Get commodity names for survey-only IDs
            survey_only_details = []
            for commodity_id in sorted(survey_only):
                if commodity_id in commodities:
                    name = commodities[commodity_id]['name']
                    survey_only_details.append(f"{commodity_id}:{name}")
                else:
                    survey_only_details.append(str(commodity_id))
            print(f'Survey-only ({len(survey_only)}): {survey_only_details}')

        print(f'\n=== OBSERVATIONS ===')
        for record_type, data in observations.items():
            print(f'{record_type}: {data["observations"]} observations from {data["unique_records"]} unique records')

        return {
            'commodities': commodities,
            'records': records,
            'observations': observations,
            'etl_tracking': etl_tracking,
            'parameters_units': parameters_units
        }

class CommodityMapper:
    """Check commodity mapping functionality"""

    def __init__(self):
        self.engine = get_database_engine()

    def check_mapping_table(self) -> Dict:
        """Check resource_usda_commodity_map table with resource linkage"""
        with self.engine.connect() as conn:
            # Get mapping tiers with commodity details
            result = conn.execute(text("""
                SELECT
                    rcm.match_tier,
                    COUNT(*) as count,
                    STRING_AGG(uc.api_name, ', ') as api_names
                FROM resource_usda_commodity_map rcm
                JOIN usda_commodity uc ON rcm.usda_commodity_id = uc.id
                GROUP BY rcm.match_tier
                ORDER BY rcm.match_tier
            """))

            mappings = {}
            for row in result:
                mappings[row[0]] = {
                    'count': row[1],
                    'api_names': row[2] if row[2] else []
                }

            # Get detailed mapping with resource information
            detailed_mappings = conn.execute(text("""
                SELECT
                    rcm.match_tier,
                    uc.api_name,
                    r.name as resource_name,
                    pap.name as primary_ag_product_name
                FROM resource_usda_commodity_map rcm
                JOIN usda_commodity uc ON rcm.usda_commodity_id = uc.id
                LEFT JOIN resource r ON rcm.resource_id = r.id
                LEFT JOIN primary_ag_product pap ON r.primary_ag_product_id = pap.id
                ORDER BY rcm.match_tier, uc.api_name
            """)).fetchall()

            mappings['detailed'] = detailed_mappings

            return mappings

    def get_mapped_commodity_ids(self) -> List[str]:
        """Get mapped commodity API names (same as ETL function)"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT DISTINCT uc.api_name as commodity_name
                FROM usda_commodity uc
                JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                WHERE rcm.match_tier != 'UNMAPPED'
                  AND uc.api_name IS NOT NULL
                  AND uc.api_name != ''
                ORDER BY commodity_name
            """))

            return [row[0] for row in result.fetchall()]

    def check_mapping_coverage(self) -> Dict:
        """Check mapping coverage analysis"""
        print(f"\n🔍 COMMODITY MAPPING ANALYSIS")
        print("=" * 50)

        mappings = self.check_mapping_table()
        mapped_commodities = self.get_mapped_commodity_ids()



        print(f'\n=== DETAILED COMMODITY MAPPINGS ===')
        print(f'\n For each mapped commodity, we show the API name, linked resource (if any), and primary ag product (if any). ')

        if 'detailed' in mappings:
            current_tier = None
            for row in mappings['detailed']:
                tier, api_name, resource_name, pap_name = row
                if tier != current_tier:
                    print(f'\n{tier}:')
                    current_tier = tier
                resource_info = resource_name or 'No resource'
                pap_info = pap_name or 'No primary ag product'
                print(f'  • {api_name} → {resource_info} → {pap_info}')

        print(f'\n=== MAPPED COMMODITIES FOR ETL ({len(mapped_commodities)}) ===')
        for commodity in mapped_commodities:
            print(f'  - {commodity}')

        return {
            'mappings': mappings,
            'mapped_commodities': mapped_commodities
        }

def main():
    parser = argparse.ArgumentParser(description='Comprehensive USDA ETL testing and diagnostics')
    parser.add_argument('--api', action='store_true', help='Test API connectivity only')
    parser.add_argument('--database', action='store_true', help='Check database state only')
    parser.add_argument('--mapping', action='store_true', help='Check commodity mappings only')
    parser.add_argument('--all', action='store_true', help='Run all tests')

    args = parser.parse_args()

    # Default to all if no specific test requested
    if not any([args.api, args.database, args.mapping]):
        args.all = True

    print("🚀 COMPREHENSIVE USDA ETL DIAGNOSTICS")
    print("=" * 60)

    try:
        if args.api or args.all:
            mapper = CommodityMapper()
            mapped_commodities = mapper.get_mapped_commodity_ids()

            tester = USDAAPITester()
            api_results = tester.comprehensive_api_test(mapped_commodities)

        if args.database or args.all:
            analyzer = DatabaseAnalyzer()
            db_results = analyzer.comprehensive_database_analysis()

        if args.mapping or args.all:
            mapper = CommodityMapper()
            mapping_results = mapper.check_mapping_coverage()

        print(f"\n✅ DIAGNOSTICS COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"\n❌ DIAGNOSTICS FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
