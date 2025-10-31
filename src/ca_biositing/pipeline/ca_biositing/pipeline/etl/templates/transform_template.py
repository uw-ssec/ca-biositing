"""
ETL Transform Template (Advanced)
---

This module provides a template for transforming data from one or more sources.

To use this template:
1.  Copy this file to the appropriate subdirectory in `src/etl/transform/`.
    For example: `src/etl/transform/new_module/new_data.py`
2.  Update `EXTRACT_SOURCES` to list the names of the extract modules that
    this transformation depends on.
3.  Update the placeholder logic in the `transform` function to implement the
    specific data validation and transformation required.
"""

from typing import Optional, Dict, List
import pandas as pd
from prefect import task, get_run_logger

# --- CONFIGURATION ---
# TODO: List the names of the extract modules this transform depends on.
# The pipeline runner will provide the output of these extract functions
# in the `data_sources` dictionary.
EXTRACT_SOURCES: List[str] = ["source_one", "source_two"]


@task
def transform(data_sources: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Transforms raw data from multiple sources into a structured and clean format.

    This function serves as the 'Transform' step in an ETL pipeline.

    Args:
        data_sources (Dict[str, pd.DataFrame]): A dictionary where keys are the
                      names of the extract sources and values are the
                      DataFrames they produced.

    Returns:
        A DataFrame containing the transformed and cleaned data, ready for
        loading, or None if validation fails.
    """
    logger = get_run_logger()
    logger.info("Transforming raw data from multiple sources...")

    # --- 1. Input Validation ---
    # Check if all required data sources are present
    for source_name in EXTRACT_SOURCES:
        if source_name not in data_sources:
            logger.error(f"Required data source '{source_name}' not found.")
            return None

    # TODO: Define the columns required from each data source.
    required_columns = {
        "source_one": ["column_a", "column_b"],
        "source_two": ["column_c", "column_d"],
    }

    # Check if all required columns exist in their respective DataFrames
    for source_name, columns in required_columns.items():
        df = data_sources[source_name]
        for col in columns:
            if col not in df.columns:
                logger.error(f"Required column '{col}' not found in source '{source_name}'.")
                return None

    # --- 2. Data Transformation ---
    # TODO: Implement the specific data transformation logic here.
    # This may include:
    #   - Merging or joining DataFrames from different sources.
    #   - Renaming columns.
    #   - Handling missing values.
    #   - Creating new, calculated columns.

    # Example placeholder logic:
    # df1 = data_sources['source_one']
    # df2 = data_sources['source_two']
    # merged_df = pd.merge(df1, df2, on='common_join_key', how='inner')
    # transformed_df = merged_df.copy()

    # For this template, we will just return the first DataFrame as is.
    # Replace this with your actual transformation logic.
    transformed_df = data_sources[EXTRACT_SOURCES[0]].copy()

    logger.info(f"Successfully transformed data. Result has {len(transformed_df)} records.")

    return transformed_df
