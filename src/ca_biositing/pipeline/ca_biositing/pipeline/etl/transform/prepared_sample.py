"""
ETL Transform for Prepared Sample
---
This module transforms raw preparation data into the prepared_sample table format.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

# --- CONFIGURATION ---
EXTRACT_SOURCES: List[str] = ["preparation"]

@task
def transform(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: int = None,
    lineage_group_id: int = None
) -> Optional[pd.DataFrame]:
    """
    Transforms raw preparation data into a structured format for the prepared_sample table.

    Args:
        data_sources: Dictionary where keys are source names and values are DataFrames.
        etl_run_id: ID of the current ETL run.
        lineage_group_id: ID of the lineage group.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
    from ca_biositing.datamodels.models import (
        FieldSample,
        PreparationMethod,
        Contact
    )

    # 1. Input Validation
    source_name = "preparation"
    if source_name not in data_sources:
        logger.error(f"Required data source '{source_name}' not found.")
        return None

    df = data_sources[source_name].copy()
    if df.empty:
        logger.warning(f"Data source '{source_name}' is empty.")
        return pd.DataFrame()

    logger.info(f"Transforming {len(df)} rows from '{source_name}'")

    # 2. Cleaning & Coercion
    # Standardize column names (snake_case) and basic string cleaning
    cleaned_df = cleaning_mod.standard_clean(df)

    # Coerce data types based on notebook logic
    # Note: Notebook mentioned issues with float columns due to commas,
    # coercion_mod.coerce_columns should handle basic numeric conversion.
    coerced_df = coercion_mod.coerce_columns(
        cleaned_df,
        int_cols=[],
        float_cols=['prep_temp_c', 'amount_before_drying_g', 'amount_after_drying_g', 'amount_remaining_g'],
        datetime_cols=['preparation_date', 'amount_as_of_date'],
        bool_cols=['drying_step']
    )

    # 3. Normalization (Name-to-ID Swapping)
    # Format: 'dataframe_column': (SQLAlchemyModel, 'lookup_field_in_db')
    normalize_columns = {
        'sample_name': (FieldSample, 'name'),
        'preparation_method': (PreparationMethod, 'name'),
        'analyst_email': (Contact, 'email')
    }

    logger.info("Normalizing data (swapping names for IDs)...")
    normalized_df = normalize_dataframes(coerced_df, normalize_columns)

    # 4. Column Renaming & Selection
    # Based on notebook:
    # preparation_selected = preparation_coerced[['prepared_sample', #prepared_sample.name
    #                                             'sample_name', #field_sample.name
    #                                             'preparation_method', #prep_method_id -> preparation_method.name
    #                                             'preparation_date', #prep_date
    #                                             'analyst_email', #preparer_id -> contact.email
    #                                             'note']] #note

    rename_map = {
        'prepared_sample': 'name',
        'sample_name_id': 'field_sample_id',
        'preparation_method_id': 'prep_method_id',
        'preparation_date': 'prep_date',
        'analyst_email_id': 'preparer_id',
        'note': 'note'
    }

    # Add lineage tracking metadata
    normalized_df['etl_run_id'] = etl_run_id
    normalized_df['lineage_group_id'] = lineage_group_id

    # Select and rename
    available_cols = [c for c in rename_map.keys() if c in normalized_df.columns]
    final_rename = {k: v for k, v in rename_map.items() if k in available_cols}

    final_df = normalized_df[available_cols].copy().rename(columns=final_rename)

    # Ensure lineage columns are in the final selection
    if etl_run_id:
        final_df['etl_run_id'] = etl_run_id
    if lineage_group_id:
        final_df['lineage_group_id'] = lineage_group_id

    logger.info(f"Successfully transformed {len(final_df)} records for prepared_sample.")
    return final_df
