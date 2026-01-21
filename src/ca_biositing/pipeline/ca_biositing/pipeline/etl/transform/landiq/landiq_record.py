"""
ETL Transform for Land IQ Data
---

This module provides functionality for transforming Land IQ GeoDataFrames into the LandiqRecord table format.
"""

import pandas as pd
import geopandas as gpd
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

@task
def transform_landiq_record(
    gdf: gpd.GeoDataFrame,
    etl_run_id: str = None,
    lineage_group_id: int = None
) -> pd.DataFrame:
    """
    Transforms Land IQ GeoDataFrame into the LandiqRecord table format.

    Args:
        gdf: Raw GeoDataFrame from Land IQ shapefile.
        etl_run_id: ID of the current ETL run.
        lineage_group_id: ID of the lineage group.

    Returns:
        A pandas DataFrame formatted for the landiq_record table.
    """
    from ca_biositing.datamodels.schemas.generated.ca_biositing import (
        Dataset,
        Polygon,
        PrimaryAgProduct,
    )

    logger = get_run_logger()
    logger.info("Transforming Land IQ data for LandiqRecord table")

    if gdf is None or gdf.empty:
        logger.error("Input GeoDataFrame is empty or None")
        return pd.DataFrame()

    # 1. Initial Cleaning & Preparation
    # Convert GeoDataFrame to regular DataFrame to avoid issues with standard_clean
    df = pd.DataFrame(gdf.copy())

    # Set dataset name and version as requested
    df['dataset'] = 'landiq'
    df['version'] = 'land use 2023'

    # Map shapefile columns to model fields
    # CLASS2 is the main crop for single cropped fields
    if 'CLASS2' in df.columns:
        df['main_crop'] = df['CLASS2']
    if 'CLASS1' in df.columns:
        df['secondary_crop'] = df['CLASS1']
    if 'CLASS3' in df.columns:
        df['tertiary_crop'] = df['CLASS3']
    if 'CLASS4' in df.columns:
        df['quaternary_crop'] = df['CLASS4']

    # Map UniqueID to record_id for lineage and upsert
    if 'UniqueID' in df.columns:
        df['record_id'] = df['UniqueID']
    elif 'UNIQUEID' in df.columns:
        df['record_id'] = df['UNIQUEID']

    # Handle Irrigation status (IRR_TYP1PA/IRR_TYP2PA etc)
    if 'IRR_TYP1PA' in df.columns:
        df['irrigated'] = df['IRR_TYP1PA'].astype(str).str.lower().str.contains('irrigated')
    else:
        df['irrigated'] = False

    # 2. Standard Clean
    # We pass lowercase=False because standard_clean's to_lowercase_df implementation
    # has a bug where it tries to access .str on the DataFrame itself if columns is None.
    # 2. Standard Clean
    # We pass lowercase=False and replace_empty=False to avoid bugs in cleaning.py
    # that occur when processing DataFrames with certain column types.
    cleaned_df = cleaning_mod.clean_names_df(df)

    # Remove duplicate columns if any (e.g., if 'main_crop' already existed)
    cleaned_df = cleaned_df.loc[:, ~cleaned_df.columns.duplicated()].copy()

    # Manually lowercase string columns and handle empty strings
    # We iterate over columns and check if they are string-like to avoid AttributeError
    for i in range(len(cleaned_df.columns)):
        # Use iloc with integer index to handle potential duplicate column names
        # which can cause .loc to return a DataFrame instead of a Series
        series = cleaned_df.iloc[:, i]

        if series.dtype == "object" or pd.api.types.is_string_dtype(series):
            # Use Series-level .str accessor explicitly
            cleaned_df.iloc[:, i] = series.astype(str).str.lower().replace(r"^\s*$", None, regex=True)

    # Add lineage IDs
    if etl_run_id:
        cleaned_df['etl_run_id'] = etl_run_id
    if lineage_group_id:
        cleaned_df['lineage_group_id'] = lineage_group_id

    # 3. Coercion
    coerced_df = coercion_mod.coerce_columns(
        cleaned_df,
        float_cols=['acres'],
        int_cols=['confidence'] if 'confidence' in cleaned_df.columns else []
    )

    # 4. Normalization
    # We need to map names to IDs for related tables
    # We also normalize polygons using the geometry (WKT) as the identifier
    normalize_columns = {
        'dataset': (Dataset, 'name'),
        'main_crop': (PrimaryAgProduct, 'name'),
        'secondary_crop': (PrimaryAgProduct, 'name'),
        'tertiary_crop': (PrimaryAgProduct, 'name'),
        'quaternary_crop': (PrimaryAgProduct, 'name'),
        'geometry': (Polygon, 'geom'),
    }

    # Ensure geometry is in WKT format for normalization if it's a GeoSeries
    if 'geometry' in coerced_df.columns and hasattr(coerced_df['geometry'], 'to_wkt'):
        coerced_df['geometry'] = coerced_df['geometry'].to_wkt()

    normalized_df = normalize_dataframes(coerced_df, normalize_columns)

    # 5. Table Specific Mapping
    rename_map = {
        'record_id': 'record_id',
        'acres': 'acres',
        'version': 'version',
        'etl_run_id': 'etl_run_id',
        'lineage_group_id': 'lineage_group_id',
        'irrigated': 'irrigated',
        'confidence': 'confidence'
    }

    # Add normalized ID columns
    for col in normalize_columns.keys():
        norm_col = f"{col}_id"
        if norm_col in normalized_df.columns:
            # Special case: geometry_id maps to polygon_id in LandiqRecord
            target_col = 'polygon_id' if col == 'geometry' else norm_col
            rename_map[norm_col] = target_col

    # Ensure dataset_id is included if it was normalized
    if 'dataset_id' in normalized_df.columns:
        rename_map['dataset_id'] = 'dataset_id'

    available_cols = [c for c in rename_map.keys() if c in normalized_df.columns]
    final_rename = {k: v for k, v in rename_map.items() if k in available_cols}

    try:
        record_df = normalized_df[available_cols].copy().rename(columns=final_rename)

        # Ensure record_id exists for lineage tracking
        if 'record_id' in record_df.columns:
            record_df = record_df.dropna(subset=['record_id'])
        else:
            logger.warning("record_id (UniqueID) missing from Land IQ transform")

        # Add geometry for polygon handling in load step
        if 'geometry' in gdf.columns:
            record_df['geometry'] = gdf['geometry'].values

        logger.info(f"Successfully transformed {len(record_df)} Land IQ records")
        return record_df

    except Exception as e:
        logger.error(f"Error during Land IQ transform: {e}", exc_info=True)
        return pd.DataFrame()
