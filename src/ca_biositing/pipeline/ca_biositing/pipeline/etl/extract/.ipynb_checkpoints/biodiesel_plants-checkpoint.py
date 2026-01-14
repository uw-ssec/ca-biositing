from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
from ...utils.gdrive_to_pandas import gdrive_to_df
# from resources.prefect import credentials

@task
def extract(csv_path) -> Optional[pd.DataFrame]:
    """
    Extracts raw data from a .csv file.

    This function serves as the 'Extract' step in an ETL pipeline. It connects
    to the data source and returns the data as is, without transformation.

    Returns:
        A pandas DataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()

    FILE_NAME = "Biodiesel_Plants.csv"
    CREDENTIALS_PATH = "credentials.json"
    logger.info(f"Extracting raw data from '{FILE_NAME}'...")

    # The gsheet_to_df function handles authentication, data fetching, and error handling.
    raw_df = gdrive_to_pandas(FILE_NAME, CREDENTIALS_PATH)



    if raw_df is None:
        logger.error("Failed to extract data. Aborting.")
        return None

    logger.info("Successfully extracted raw data.")
    return raw_df
