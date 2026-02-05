"""
USDA NASS Census and Survey Data Extraction

This module provides a function to extract agricultural data from the USDA NASS
Quick Stats API and convert it into a pandas DataFrame.

The USDA QuickStats API documentation:
https://quickstats.nass.usda.gov/api

API Key Setup:
1. Go to https://quickstats.nass.usda.gov/api and request a free API key
2. Set environment variable: USDA_NASS_API_KEY=your_key_here
"""

import os
import requests
import pandas as pd
from typing import Optional, List
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configuration
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET"
TIMEOUT = 30
MAX_RETRIES = 3
# Rate limiting: USDA API has implicit rate limits.
# Being respectful: 1 second between requests
REQUEST_DELAY = 1.0


def _get_session_with_retries():
    """
    Create a requests session with retry strategy for API resilience.

    This uses exponential backoff to respect the NASS API:
    - Retry on: 429 (rate limit), 500-504 (server errors)
    - Backoff: 2^attempt seconds (1s, 2s, 4s, 8s...)
    - Max retries: 3

    This respects NASS API terms by not hammering the endpoint.

    Returns:
        requests.Session: Session with retry strategy configured
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,  # Exponential backoff: 2^attempt seconds
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def usda_nass_to_df(
    api_key: str,
    state: str = "CA",
    year: Optional[int] = None,
    commodity: Optional[str] = None,
    commodity_ids: Optional[List[int]] = None,
    county_code: Optional[str] = None,
    agg_level_desc: str = "COUNTY",
    statisticcat_desc: Optional[str] = None,
    unit_desc: Optional[str] = None,
    domain_desc: str = "TOTAL",
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Fetch agricultural data from USDA NASS QuickStats API with detailed filtering.

    This function queries the USDA NASS API for agricultural census and survey data.
    It supports filtering by state, year, commodity, county, aggregation level,
    statistic category, units, and domain.

    Args:
        api_key (str): Your USDA NASS API key
        state (str): State code (e.g., "CA"). Default: "CA"
        year (Optional[int]): Filter by specific year. Default: None (all years)
        commodity (Optional[str]): Commodity name (e.g., "CORN", "ALMONDS")
        commodity_ids (Optional[List[str]]): USDA commodity names from database (e.g., ["CORN", "WHEAT"])
        county_code (Optional[str]): County FIPS code (e.g., "06077" for San Joaquin)
        agg_level_desc (str): Aggregation level - "NATIONAL", "STATE", "COUNTY", "DISTRICT"
                             Default: "COUNTY"
        statisticcat_desc (Optional[str]): "AREA HARVESTED", "YIELD", "PRODUCTION", etc.
        unit_desc (Optional[str]): "ACRES", "BUSHELS", "TONS", etc.
        domain_desc (str): "TOTAL" (all operations) or specific demographic subset
                          Default: "TOTAL"
        **kwargs: Additional NASS API parameters

    Returns:
        Optional[pd.DataFrame]: DataFrame with columns including record count tracking

    Reference:
        https://quickstats.nass.usda.gov/api
        https://content.ces.ncsu.edu/getting-data-from-the-national-agricultural-statistics-service-nass-using-r

    Example:
        >>> df = usda_nass_to_df(
        ...     api_key="your_key",
        ...     state="CA",
        ...     year=2023,
        ...     commodity="CORN",
        ...     county_code="06077",  # San Joaquin County
        ...     agg_level_desc="COUNTY",
        ...     statisticcat_desc="YIELD",
        ...     unit_desc="BUSHELS"
        ... )
    """

    if not api_key:
        print("Error: USDA_NASS_API_KEY is not set. Get a free key at https://quickstats.nass.usda.gov/api")
        return None

    # Base parameters for all requests
    base_params = {
        "key": api_key,
        "state_alpha": state,
        "format": "JSON",
    }

    # Add optional filters
    if year is not None:
        base_params["year"] = year
    if county_code is not None:
        base_params["county_code"] = county_code

    base_params["agg_level_desc"] = agg_level_desc
    base_params["domain_desc"] = domain_desc

    if statisticcat_desc is not None:
        base_params["statisticcat_desc"] = statisticcat_desc
    if unit_desc is not None:
        base_params["unit_desc"] = unit_desc

    # Add any additional kwargs
    base_params.update(kwargs)

    session = _get_session_with_retries()
    all_dfs = []
    total_records_imported = 0
    query_log = []

    try:
        # Handle commodity_ids query (database-driven approach)
        if commodity_ids is not None:
            if not commodity_ids:
                print("Warning: commodity_ids list is empty. No data to fetch.")
                return pd.DataFrame()

            print(f"Querying USDA API for {len(commodity_ids)} commodities...")

            for idx, commodity_name in enumerate(commodity_ids, 1):
                print(f"  [{idx}/{len(commodity_ids)}] Fetching commodity: {commodity_name}...")

                # Create params for this commodity
                params = base_params.copy()
                params["commodity_desc"] = commodity_name

                try:
                    response = session.get(BASE_URL, params=params, timeout=TIMEOUT)
                    response.raise_for_status()

                    data = response.json()

                    # Check for API errors
                    if isinstance(data, dict) and "error" in data:
                        print(f"    USDA API Error: {data['error']}")
                        continue

                    # Extract actual data (USDA API returns {"data": [...]} not [...])
                    if isinstance(data, dict) and "data" in data:
                        actual_data = data["data"]
                    elif isinstance(data, list):
                        actual_data = data
                    else:
                        actual_data = []

                    # Check if we have data (successful query)
                    if len(actual_data) > 0:
                        df = pd.DataFrame(actual_data)
                        all_dfs.append(df)
                        records_count = len(df)
                        total_records_imported += records_count
                        query_log.append({
                            'commodity_name': commodity_name,
                            'records': records_count,
                            'year': year,
                            'status': 'success'
                        })
                        print(f"    [OK] Retrieved {records_count} records for commodity {commodity_name}")
                    else:
                        query_log.append({
                            'commodity_name': commodity_name,
                            'records': 0,
                            'year': year,
                            'status': 'no_data'
                        })
                        print(f"    No data returned for commodity {commodity_name}")

                    # Rate limiting (NASS API courtesy)
                    # Being respectful to avoid key suspension
                    time.sleep(REQUEST_DELAY)

                except requests.exceptions.RequestException as e:
                    print(f"    Request failed for commodity {commodity_name}: {e}")
                    continue

        # Handle commodity name query (fallback)
        elif commodity is not None:
            print(f"Querying USDA API for commodity: {commodity}")
            params = base_params.copy()
            params["commodity_desc"] = commodity

            try:
                response = session.get(BASE_URL, params=params, timeout=TIMEOUT)
                response.raise_for_status()

                data = response.json()

                if isinstance(data, dict) and "error" in data:
                    print(f"USDA API Error: {data['error']}")
                    return None

                # Extract actual data (USDA API returns {"data": [...]} not [...])
                if isinstance(data, dict) and "data" in data:
                    actual_data = data["data"]
                elif isinstance(data, list):
                    actual_data = data
                else:
                    actual_data = []

                if len(actual_data) > 0:
                    df = pd.DataFrame(actual_data)
                    all_dfs.append(df)
                    print(f"✓ Retrieved {len(df)} records for commodity {commodity}")
                else:
                    print(f"No data returned for commodity {commodity}")

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return None

        # Query all data (no commodity filter)
        else:
            print("Querying USDA API for all commodities in state...")
            try:
                response = session.get(BASE_URL, params=base_params, timeout=TIMEOUT)
                response.raise_for_status()

                data = response.json()

                if isinstance(data, dict) and "error" in data:
                    print(f"USDA API Error: {data['error']}")
                    return None

                # Extract actual data (USDA API returns {"data": [...]} not [...])
                if isinstance(data, dict) and "data" in data:
                    actual_data = data["data"]
                elif isinstance(data, list):
                    actual_data = data
                else:
                    actual_data = []

                if len(actual_data) > 0:
                    df = pd.DataFrame(actual_data)
                    all_dfs.append(df)
                    print(f"✓ Retrieved {len(df)} total records")
                else:
                    print("No data returned from API")

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                return None

        # Combine all DataFrames if multiple queries were made
        if len(all_dfs) == 0:
            print("No data retrieved from USDA API.")
            return pd.DataFrame()

        if len(all_dfs) == 1:
            result_df = all_dfs[0]
        else:
            result_df = pd.concat(all_dfs, ignore_index=True)
            print(f"✓ Combined {len(all_dfs)} queries into {len(result_df)} total records")

        # Add metadata for tracking
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"Total Records Imported: {total_records_imported}")
        print(f"Parameters Used:")
        print(f"  - State: {state}")
        print(f"  - Year: {year if year else 'All'}")
        print(f"  - Aggregation Level: {agg_level_desc}")
        print(f"  - Domain: {domain_desc}")
        if statisticcat_desc:
            print(f"  - Statistic Category: {statisticcat_desc}")
        if unit_desc:
            print(f"  - Unit: {unit_desc}")
        if county_code:
            print(f"  - County Code: {county_code}")
        print("="*60 + "\n")

        return result_df

    except Exception as e:
        print(f"Unexpected error fetching USDA data: {e}")
        return None
    finally:
        session.close()


if __name__ == "__main__":
    # Example usage for testing
    api_key = os.getenv("USDA_NASS_API_KEY", "")

    if not api_key:
        print("To test this module, set USDA_NASS_API_KEY environment variable")
        print("Get a free key at: https://quickstats.nass.usda.gov/api")
    else:
        # Test query for a single commodity
        print("=== Testing USDA API with commodity name ===")
        df = usda_nass_to_df(api_key=api_key, state="CA", year=2023, commodity="CORN")
        if df is not None:
            print(f"\nResult shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"\nFirst few rows:")
            print(df.head())
