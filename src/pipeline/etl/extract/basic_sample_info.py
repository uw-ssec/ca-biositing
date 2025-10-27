from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
from src.pipeline.utils.gsheet_to_pandas import gsheet_to_df

@task
def extract_basic_sample_info() -> Optional[pd.DataFrame]:
    """
    Extracts the raw data from the '01-BasicSampleInfo' worksheet in the Google Sheet.

    This function is purely for extraction (the 'E' in ETL). It connects to the
    data source and returns the data as is, without any transformation.

    Returns:
        A pandas DataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()
    logger.info("Extracting raw data from '01-BasicSampleInfo' worksheet...")

    GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
    WORKSHEET_NAME = "01-BasicSampleInfo"
    CREDENTIALS_PATH = "credentials.json"

    raw_df = gsheet_to_df(GSHEET_NAME, WORKSHEET_NAME, CREDENTIALS_PATH)

    if raw_df is None:
        logger.error("Failed to extract data. Aborting.")
        return None

    logger.info("Successfully extracted raw data.")
    return raw_df
