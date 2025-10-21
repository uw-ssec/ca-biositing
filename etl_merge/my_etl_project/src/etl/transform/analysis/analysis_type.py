from typing import Optional, Dict
import pandas as pd
from prefect import task, get_run_logger

EXTRACT_SOURCES = ["experiments"]

@task
def transform_analysis_analysis_type(data_sources: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Transforms the raw data to extract unique analysis names.

    This function is purely for transformation (the 'T' in ETL). It takes the
    raw DataFrame and performs the specific transformations needed for the
    'analysis_types' table.

    Args:
        data_sources: A dictionary of DataFrames from the extraction step.

    Returns:
        A transformed DataFrame with a single 'analysis_name' column containing
        unique analysis_names, or None if an error occurs.
    """
    logger = get_run_logger()
    logger.info("Transforming raw data for analysis types...")

    raw_experiments_df = data_sources["experiments"]

    # Step 1: Check if the required column exists
    if 'Analysis_type' not in raw_experiments_df.columns:
        logger.error("'Analysis_type' column not found in the raw data.")
        return None

    # Step 2: Get unique product names and create the final DataFrame
    analysis_names = raw_experiments_df['Analysis_type'].unique()
    transformed_df = pd.DataFrame(analysis_names, columns=["analysis_name"])

    logger.info(f"Successfully transformed data, found {len(transformed_df)} unique analysis_names.")
    return transformed_df
