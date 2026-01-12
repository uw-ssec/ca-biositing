from typing import Optional, Dict
import pandas as pd
from prefect import task, get_run_logger

EXTRACT_SOURCES = ["basic_sample_info"]

@task
def transform(data_sources: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Transforms the raw data to extract unique primary agricultural products.

    This function is purely for transformation (the 'T' in ETL). It takes the
    raw DataFrame and performs the specific transformations needed for the
    'primary_ag_product' table.

    Args:
        data_sources: A dictionary of DataFrames from the extraction step.

    Returns:
        A transformed DataFrame with a single 'name' column containing
        unique product names, or None if an error occurs.
    """
    logger = get_run_logger()
    logger.info("Transforming raw data for primary ag products...")

    raw_df = data_sources["basic_sample_info"]

    #Step 1: Convert column names to lowercase for consistency
    raw_df.columns = [col.lower() for col in raw_df.columns]

    # Step 2: Check if the required column exists
    if 'primary_ag_product' not in raw_df.columns:
        logger.error("'primary_ag_product' column not found in the raw data.")
        return None

    # Step 3: Get unique product names and create the final DataFrame
    primary_ag_product= raw_df['primary_ag_product'].unique()
    transformed_df = pd.DataFrame(primary_ag_product, columns=["name"])

    logger.info(f"Successfully transformed data, found {len(transformed_df)} unique primary_ag_products.")
    return transformed_df
