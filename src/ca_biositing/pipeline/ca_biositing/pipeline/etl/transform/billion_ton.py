"""
ETL Transform for Billion Ton 2023 Agricultural Dataset
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

# --- CONFIGURATION ---
EXTRACT_SOURCES: List[str] = ["billion_ton"]

@task
def transform(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: int = None,
    lineage_group_id: int = None
) -> Optional[pd.DataFrame]:
    """
    Transforms raw Billion Ton data into the BillionTon2023Record format.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
    from ca_biositing.datamodels.models.resource_information import Resource, ResourceSubclass
    from ca_biositing.datamodels.models.methods_parameters_units.unit import Unit
    from ca_biositing.datamodels.models.general_analysis import Dataset

    # 1. Input Validation
    if "billion_ton" not in data_sources:
        logger.error("Required data source 'billion_ton' not found.")
        return None

    df = data_sources["billion_ton"].copy()
    if df.empty:
        logger.warning("Input DataFrame is empty.")
        return pd.DataFrame()

    # 2. Filter for California
    logger.info("Filtering for California records...")
    df = df[df["state_name"].str.lower() == "california"].copy()
    if df.empty:
        logger.warning("No California records found in the dataset.")
        return pd.DataFrame()

    # 3. Standard Cleaning
    # This will snake_case column names:
    # fips, county_square_miles, production_unit, btu_ton, etc.
    df = cleaning_mod.standard_clean(df)

    # Preserve county and state names for Place record creation in load step
    # standard_clean lowercase them
    # Remove " county" suffix from county names
    df['county'] = df['county'].str.replace(r'\s+county$', '', regex=True, case=False)
    df['state_name'] = df['state_name']

    # Add Dataset Name for normalization
    df['dataset_name'] = "billion ton 2023 report"

    # 4. GEOID/FIPS Formatting
    # Geoid should be fips, but all California fips should have a leading "0"
    logger.info("Formatting GEOID/FIPS...")
    df["geoid"] = df["fips"].astype(str).str.zfill(5)
    if not df["geoid"].str.startswith("06").all():
         logger.warning("Some GEOIDs do not start with '06' (California's state FIPS).")

    # 5. Column Renaming to match normalize_dataframes expectations and final model
    rename_map = {
        "production_unit": "production_unit_name",
        "energy_content_unit": "energy_content_unit_name",
        "production_density_dtpersqmi": "product_density_dtpersqmi", # Model uses 'product_density' instead of 'production_density'
        "price_offered": "price_offered_usd",
        "landsource": "land_source"
    }
    df = df.rename(columns=rename_map)

    # 6. Normalization (Name-to-ID Swapping)
    normalize_columns = {
        'dataset_name': (Dataset, 'name'),
        'subclass': (ResourceSubclass, 'name'),
        'resource': (Resource, 'name'),
        'production_unit_name': (Unit, 'name'),
        'energy_content_unit_name': (Unit, 'name'),
    }

    logger.info("Normalizing data (swapping names for IDs)...")
    # Note: normalize_dataframes will create new columns like subclass_id, resource_id, etc.
    df = normalize_dataframes(df, normalize_columns)

    # 7. Coercion
    df = coercion_mod.coerce_columns(
        df,
        int_cols=['production', 'btu_ton', 'production_energy_content'],
        float_cols=['county_square_miles', 'price_offered_usd', 'product_density_dtpersqmi'],
        datetime_cols=[]
    )

    # 8. Final Column Selection (BillionTon2023Record fields)
    target_columns = [
        'dataset_name_id',
        'subclass_id',
        'resource_id',
        'geoid',
        'county_square_miles',
        'model_name',
        'scenario_name',
        'price_offered_usd',
        'production',
        'production_unit_name_id', # Result of normalize_dataframes
        'btu_ton',
        'production_energy_content',
        'energy_content_unit_name_id', # Result of normalize_dataframes
        'product_density_dtpersqmi',
        'land_source',
        'etl_run_id',
        'lineage_group_id'
    ]

    # Final rename to match exact model field names
    final_rename = {
        "dataset_name_id": "dataset_id",
        "production_unit_name_id": "production_unit_id",
        "energy_content_unit_name_id": "energy_content_unit_id"
    }

    # Add lineage metadata if provided
    if etl_run_id is not None:
        df['etl_run_id'] = etl_run_id
    if lineage_group_id is not None:
        df['lineage_group_id'] = lineage_group_id

    # Filter columns that exist in the dataframe before renaming
    # We also keep county and state_name for the load step's Place creation
    cols_to_keep = [c for c in target_columns if c in df.columns] + ['county', 'state_name']
    df = df[cols_to_keep].copy()

    # Apply final rename
    df = df.rename(columns=final_rename)

    logger.info(f"Successfully transformed {len(df)} records.")
    return df
