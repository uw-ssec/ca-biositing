from typing import Optional, Dict
import pandas as pd

EXTRACT_SOURCES = ["basic_sample_info"]

def transform_products_primary_product(data_sources: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Transforms the raw data to extract unique primary products.

    This function is purely for transformation (the 'T' in ETL). It takes the
    raw DataFrame and performs the specific transformations needed for the
    'primary_product' table.

    Args:
        data_sources: A dictionary of DataFrames from the extraction step.

    Returns:
        A transformed DataFrame with a single 'Primary_crop' column containing
        unique product names, or None if an error occurs.
    """
    print("Transforming raw data for primary products...")

    raw_df = data_sources["basic_sample_info"]

    # Step 1: Check if the required column exists
    if 'Primary_crop' not in raw_df.columns:
        print("Error: 'Primary_crop' column not found in the raw data.")
        return None

    # Step 2: Get unique product names and create the final DataFrame
    primary_product_names = raw_df['Primary_crop'].unique()
    transformed_df = pd.DataFrame(primary_product_names, columns=["Primary_crop"])

    print(f"Successfully transformed data, found {len(transformed_df)} unique primary products.")
    return transformed_df
