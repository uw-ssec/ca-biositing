"""
USDA Census and Survey Data Extraction
---
This module extracts agricultural census and survey data from the USDA NASS
Quick Stats API for California.
Data includes:
- Census data (every 5 years): Complete agricultural census
- Survey data (annual): Preliminary and final agricultural estimates
The USDA API provides access to decades of historical data across many
commodities and regions.
For more information: https://quickstats.nass.usda.gov/api
"""

from typing import Optional
import os
import pandas as pd
from prefect import task, get_run_logger

# Use absolute imports that work both locally and in Docker
try:
    # Try absolute import first (works in Docker)
    from ca_biositing.pipeline.utils.usda_nass_to_pandas import usda_nass_to_df
    from ca_biositing.pipeline.utils.fetch_mapped_commodities import get_mapped_commodity_ids
except ImportError:
    # Fallback for local testing
    from src.ca_biositing.pipeline.ca_biositing.pipeline.utils.usda_nass_to_pandas import usda_nass_to_df
    from src.ca_biositing.pipeline.ca_biositing.pipeline.utils.fetch_mapped_commodities import get_mapped_commodity_ids

# --- CONFIGURATION ---
# USDA API Key - loaded from environment variable
# To set this, add to resources/docker/.env:
#   USDA_NASS_API_KEY=your_api_key_here
# Get your free API key at: https://quickstats.nass.usda.gov/api
USDA_API_KEY = os.getenv("USDA_NASS_API_KEY", "")

# State code to query (using USDA state abbreviation)
# CA = California
STATE = "CA"

# Optional: Filter by specific year. Set to None for all available years.
YEAR = None

# Optional: Filter by commodity (e.g., "CORN", "ALMONDS", "WHEAT")
# Leave as None to get all commodities
COMMODITY = None

# North San Joaquin Valley priority counties (3-digit NASS county codes)
# These match the counties used in the notebook
PRIORITY_COUNTIES = {
    "077",  # San Joaquin
    "099",  # Stanislaus
    "047",  # Merced
}


@task
def extract() -> Optional[pd.DataFrame]:
    """
    Extracts USDA data ONLY for commodities mapped in resource_usda_commodity_map
    and for priority counties (North San Joaquin Valley).
    This allows adding new crops by updating the database, no code changes needed.
    """
    logger = get_run_logger()
    logger.info("🔵 [USDA Extract] Starting...")

    # Get commodity names from database
    commodity_ids = get_mapped_commodity_ids()
    logger.info(f"🔵 [USDA Extract] Got {len(commodity_ids) if commodity_ids else 0} commodities: {commodity_ids}")

    if not commodity_ids:
        logger.error(
            "No commodity mappings found. This could mean:\n"
            "1. Resource and primary_ag_product tables are empty (run full ETL pipeline first)\n"
            "2. The CSV mapping file is missing or corrupted\n"
            "3. Auto-seeding failed (check logs above for details)"
        )
        return None

    logger.info(f"Extracting USDA data for {len(commodity_ids)} commodities in {len(PRIORITY_COUNTIES)} priority counties...")

    # Collect data for all priority counties
    all_dfs = []

    for county_code in sorted(PRIORITY_COUNTIES):
        logger.info(f"  Querying county {county_code}...")

        # Call utility with commodity names and county filter
        county_df = usda_nass_to_df(
            api_key=USDA_API_KEY,
            state=STATE,
            year=YEAR,
            commodity_ids=commodity_ids,  # Database-driven commodity names
            county_code=county_code  # Limit to this county
        )

        if county_df is not None and not county_df.empty:
            all_dfs.append(county_df)
            logger.info(f"    Got {len(county_df)} records from county {county_code}")
        else:
            logger.warning(f"    No data for county {county_code}")

    if not all_dfs:
        logger.error("No data retrieved from any county. Aborting.")
        return None

    # Combine all counties
    raw_df = pd.concat(all_dfs, ignore_index=True)
    logger.info(f"Successfully extracted {len(raw_df)} total records from USDA NASS API across {len(all_dfs)} counties.")

    # 🔍 DIAGNOSTIC: Save raw extracted data for inspection
    try:
        debug_csv_path = "/app/data/usda_raw_extracted.csv"
        raw_df.to_csv(debug_csv_path, index=False)
        logger.info(f"💾 Debug: Raw extracted data saved to {debug_csv_path}")
        logger.info(f"📊 Raw data shape: {raw_df.shape}")
        logger.info(f"📊 Columns: {list(raw_df.columns)}")

        # Show what commodities and statistics are in the raw data
        if 'commodity_desc' in raw_df.columns:
            commodities = raw_df['commodity_desc'].unique()
            logger.info(f"🌾 Commodities in raw data: {len(commodities)}")
            for comm in sorted(commodities):
                count = len(raw_df[raw_df['commodity_desc'] == comm])
                logger.info(f"  {comm}: {count} records")

        if 'short_desc' in raw_df.columns:
            statistics = raw_df['short_desc'].str.extract(r'- (\w+(?:\s+\w+)?)\s*$')[0].unique()
            logger.info(f"📈 Statistics types in raw data: {len([s for s in statistics if s])}")
    except Exception as e:
        logger.warning(f"Could not save debug CSV: {e}")

    return raw_df
