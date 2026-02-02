"""
ETL Transform for FieldSample
---
Refactored from sampling_data_notebook.ipynb
Includes join with provider_info.
"""

import pandas as pd
from typing import List, Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

# List the names of the extract modules this transform depends on.
EXTRACT_SOURCES: List[str] = ["samplemetadata", "provider_info"]

@task
def transform_field_sample(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: int = None,
    lineage_group_id: int = None
) -> Optional[pd.DataFrame]:
    """
    Transforms raw sample metadata and provider info into the FieldSample table format.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
    from ca_biositing.datamodels.schemas.generated.ca_biositing import (
        Resource,
        Provider,
        Contact,
        Unit,
        Dataset,
        SoilType,
        LocationAddress,
        PrimaryAgProduct,
        PreparedSample,
        Method,
        FieldStorageMethod
    )

    # 1. Input Validation
    for source in EXTRACT_SOURCES:
        if source not in data_sources:
            logger.error(f"Required data source '{source}' not found.")
            return None

    metadata_df = data_sources["samplemetadata"].copy()
    provider_df = data_sources["provider_info"].copy()

    if metadata_df.empty:
        logger.warning("Source 'samplemetadata' is empty.")
        return pd.DataFrame()

    logger.info("Transforming FieldSample data with Provider join...")

    # 2. Cleaning & Coercion
    # Apply dataset tag and clean both
    metadata_df['dataset'] = 'biocirv'
    provider_df['dataset'] = 'biocirv'

    clean_metadata = cleaning_mod.standard_clean(metadata_df)
    clean_provider = cleaning_mod.standard_clean(provider_df)

    # Coerce metadata
    coerced_metadata = coercion_mod.coerce_columns(
        clean_metadata,
        int_cols=['qty'],
        float_cols=['particle_width', 'particle_length', 'particle_height'],
        datetime_cols=['fv_date_time', 'sample_ts', 'prod_date', 'created_at', 'updated_at']
    )

    # Coerce provider
    coerced_provider = coercion_mod.coerce_columns(
        clean_provider,
        datetime_cols=['created_at', 'updated_at']
    )

    # 3. Join Logic (from notebook)
    joined_df = coerced_metadata.merge(
        coerced_provider,
        on='provider_codename',
        how='left',
        suffixes=('', '_provider')
    )

    # 4. Normalization (Name-to-ID Swapping)
    normalize_columns = {
        'resource': (Resource, 'name'),
        'provider_codename': (Provider, 'codename'),
        'primary_collector': (Contact, 'name'),
        'storage_dur_units': (Unit, 'name'),
        'particle_units': (Unit, 'name'),
        'sample_unit': (Unit, 'name'),
        'prepared_sample': (PreparedSample, 'name'),
        'soil_type': (SoilType, 'name'),
        'storage_mode': (FieldStorageMethod, 'name'),
        'field_storage_method': (FieldStorageMethod, 'name'),
        'field_storage_mode': (FieldStorageMethod, 'name'),
        'county': (LocationAddress, 'county'),
        'primary_ag_product': (PrimaryAgProduct, 'name'),
        'provider_type': (Provider, 'type'),
        'dataset': (Dataset, 'name'),
        'field_storage_location': (LocationAddress, 'full_address'),
    }

    logger.info("Normalizing joined data (swapping names for IDs)...")
    normalized_df = normalize_dataframes(joined_df, normalize_columns)

    # 5. Select and Rename Columns (from notebook)
    rename_map = {
        'field_sample_name': 'name',
        'resource_id': 'resource_id',
        'provider_codename_id': 'provider_id',
        'primary_collector_id': 'collector_id',
        'sample_source': 'sample_collection_source',
        'qty': 'qty',
        'sample_unit_id': 'amount_collected_unit_id',
        'county_id': 'sampling_location_id',
        'storage_mode_id': 'field_storage_method_id',
        'field_storage_method_id': 'field_storage_method_id',
        'field_storage_mode_id': 'field_storage_method_id',
        'storage_dur_value': 'field_storage_duration_value',
        'storage_dur_units_id': 'field_storage_duration_unit_id',
        'field_storage_location_id': 'field_storage_location_id',
        'sample_ts': 'collection_timestamp',
        'sample_notes': 'note'
    }

    # Filter rename_map to only include columns that exist in normalized_df
    available_rename = {k: v for k, v in rename_map.items() if k in normalized_df.columns}

    try:
        final_df = normalized_df[list(available_rename.keys())].rename(columns=available_rename).assign(
            collection_method=None,
            harvest_datemethod=None,
            harvest_date=None,
            field_sample_storage_location_id_2=None
        )

        # 6. Lineage Tracking
        if etl_run_id:
            final_df['etl_run_id'] = etl_run_id
        if lineage_group_id:
            final_df['lineage_group_id'] = lineage_group_id

        if 'dataset_id' in normalized_df.columns:
            final_df['dataset_id'] = normalized_df['dataset_id']

        logger.info(f"Successfully transformed {len(final_df)} FieldSample records.")
        return final_df

    except Exception as e:
        logger.error(f"Error during FieldSample transform: {e}")
        return pd.DataFrame()
