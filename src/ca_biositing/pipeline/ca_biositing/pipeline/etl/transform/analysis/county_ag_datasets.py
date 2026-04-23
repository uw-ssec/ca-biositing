"""
ETL Transform for County Ag Datasets.

Transforms raw data from Sheet 07.7b into Dataset format.
Each county ag report is treated as a distinct dataset.
"""

import pandas as pd
from typing import List, Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod

# List the names of the extract modules this transform depends on.
EXTRACT_SOURCES: List[str] = ["pp_data_sources"]

@task
def transform_county_ag_datasets(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None
) -> Optional[pd.DataFrame]:
    """
    Transforms raw data source information into Dataset format.

    Args:
        data_sources: Dictionary where keys are source names and values are DataFrames.
        etl_run_id: ID of the current ETL run.
        lineage_group_id: ID of the lineage group.

    Returns:
        Transformed DataFrame ready for loading into the Dataset table.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    # 1. Input Validation
    if "pp_data_sources" not in data_sources:
        logger.error("Required data source 'pp_data_sources' not found.")
        return None

    df = data_sources["pp_data_sources"].copy()
    if df is None or df.empty:
        logger.warning("Data source 'pp_data_sources' is empty.")
        return pd.DataFrame()

    logger.info("Transforming county ag datasets...")

    # 2. Cleaning
    # Avoid standard_clean for this reference sheet to maintain control over names
    # Manually clean names to snake_case
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]

    # 3. Filter empty rows
    if 'index' not in df.columns:
        logger.error(f"Column 'index' not found. Columns: {df.columns.tolist()}")
        return pd.DataFrame()

    df = df[df['index'].notna() & (df['index'] != "")]

    if df.empty:
        logger.warning("No valid data sources found after filtering empty rows.")
        return pd.DataFrame()

    # 4. Map to Dataset Fields
    # Dataset fields: name, record_type, source_id, description
    df['record_type'] = "county_ag_report_record"

    # Determine the correct column for SourceName
    src_col = 'sourcename' if 'sourcename' in df.columns else ('source_name' if 'source_name' in df.columns else None)

    # Generate a clean dataset name from the source name
    def clean_name(row):
        val = row.get(src_col) if src_col else "UNKNOWN"
        if pd.isna(val):
            val = "UNKNOWN"
        name = str(val).upper().replace(' ', '_').replace(',', '')
        return name

    df['name'] = df.apply(clean_name, axis=1)
    df['source_id'] = pd.to_numeric(df['index'], errors='coerce').astype(int)

    if src_col:
        df['description'] = df[src_col]
    else:
        df['description'] = "Unknown Source"

    # 5. Final Preparation
    df["etl_run_id"] = etl_run_id
    df["lineage_group_id"] = lineage_group_id

    model_columns = [
        "name", "record_type", "source_id", "description", "etl_run_id", "lineage_group_id"
    ]

    # Ensure columns exist
    for col in model_columns:
        if col not in df.columns:
            df[col] = None

    final_df = df[model_columns]

    logger.info(f"Transformed {len(final_df)} datasets.")
    return final_df
