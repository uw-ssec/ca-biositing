from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
import os

@task
def extract(file_path: str) -> Optional[pd.DataFrame]:
    """
    Extracts raw data from a local .csv file.

    Returns:
        A pandas DataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()

    logger.info(f"Extracting raw data from '{file_path}'...")

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    try:
        raw_df = pd.read_csv(file_path)
        logger.info(f"Successfully extracted {len(raw_df)} rows from raw data.")
        return raw_df
    except Exception as e:
        logger.error(f"Failed to extract data from {file_path}: {e}")
        return None
