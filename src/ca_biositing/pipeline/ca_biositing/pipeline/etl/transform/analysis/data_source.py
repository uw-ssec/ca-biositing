"""
ETL Transform for Data Sources.

Transforms raw data from Sheet 07.7b into DataSource format.
"""

import pandas as pd
from typing import List, Optional, Dict
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod

# List the names of the extract modules this transform depends on.
EXTRACT_SOURCES: List[str] = ["pp_data_sources"]

@task
def transform_data_sources(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None
) -> Optional[pd.DataFrame]:
    """
    Transforms raw data source information into DataSource format.

    Args:
        data_sources: Dictionary where keys are source names and values are DataFrames.
        etl_run_id: ID of the current ETL run.
        lineage_group_id: ID of the lineage group.

    Returns:
        Transformed DataFrame ready for loading into the DataSource table.
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
    if df.empty:
        logger.warning("Data source 'pp_data_sources' is empty.")
        return pd.DataFrame()

    logger.info("Transforming data sources...")

    # 2. Standard Cleaning
    # This converts 'Index' to 'index', 'SourceName' to 'source_name', etc.
    df = cleaning_mod.standard_clean(df)

    # 3. Filter empty rows (Sheet 07.7b has 50 rows but many are empty)
    df = df[df['index'].notna() & (df['index'] != "")]

    # 4. Map to Model Fields
    # Model fields: id, name, full_title, creator, date, uri
    rename_map = {
        "index": "id",
        "source_name": "name",
        "author": "creator",
        "url": "uri"
    }
    df = df.rename(columns=rename_map)

    # Convert id to int
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype(int)

    # Handle date (it's a year string/int in the sheet)
    def clean_date(val):
        if pd.isna(val) or str(val).strip() == "":
            return None
        try:
            year = int(float(val))
            import datetime
            return datetime.datetime(year, 1, 1)
        except (ValueError, TypeError):
            return None

    df['date'] = df['date'].apply(clean_date)

    # 5. Final Preparation
    df["etl_run_id"] = etl_run_id
    df["lineage_group_id"] = lineage_group_id

    model_columns = [
        "id", "name", "creator", "date", "uri", "etl_run_id", "lineage_group_id"
    ]

    final_df = df[[col for col in model_columns if col in df.columns]]

    logger.info(f"Transformed {len(final_df)} data sources.")
    return final_df
