"""
ETL Transform for LocationAddress
---
Transforms raw sample metadata into unique LocationAddress records.
"""

import pandas as pd
from typing import Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod

@task
def transform_location_address(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: int = None,
    lineage_group_id: int = None
) -> Optional[pd.DataFrame]:
    """
    Extracts unique locations from sample metadata.
    Mappings to geography_ids are now handled during the loading phase
    to avoid database connections during transformation (which breaks tests).
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    source_name = "samplemetadata"
    if source_name not in data_sources:
        logger.error(f"Required data source '{source_name}' not found.")
        return None

    df = data_sources[source_name].copy()
    if df.empty:
        logger.warning(f"Data source '{source_name}' is empty.")
        return pd.DataFrame()

    logger.info(f"Extracting locations from {len(df)} sample metadata rows...")

    # Standard clean
    cleaned_df = cleaning_mod.standard_clean(df)

    # We want unique combinations of location info
    # Based on extracted columns: 'sampling_location', 'sampling_street', 'sampling_city', 'sampling_zip'
    location_cols = ['sampling_location', 'sampling_street', 'sampling_city', 'sampling_zip']
    available_cols = [c for c in location_cols if c in cleaned_df.columns]

    if not available_cols:
        logger.warning("No location columns found in metadata.")
        locations = pd.DataFrame()
    else:
        # Get unique locations
        locations = cleaned_df[available_cols].drop_duplicates().dropna(how='all')

        if locations.empty:
            logger.info("No unique locations found.")
            locations = pd.DataFrame()
        else:
            # Rename mapping to match LocationAddress model where possible
            rename_map = {
                'sampling_street': 'address_line1',
                'sampling_city': 'city',
                'sampling_zip': 'zip'
            }
            available_rename = {k: v for k, v in rename_map.items() if k in locations.columns}
            locations = locations.rename(columns=available_rename)

            # Add some defaults
            locations['is_anonymous'] = True

    # Add lineage tracking metadata
    if etl_run_id:
        locations['etl_run_id'] = etl_run_id
    if lineage_group_id:
        locations['lineage_group_id'] = lineage_group_id

    logger.info(f"Successfully transformed {len(locations)} unique location candidate records.")
    return locations
