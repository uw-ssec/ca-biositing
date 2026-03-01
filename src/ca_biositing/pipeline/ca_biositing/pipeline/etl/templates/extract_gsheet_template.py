"""
ETL Extract Template.


This module provides a template for extracting data from a Google Sheet.

To use this template:
1.  Copy this file to the appropriate subdirectory in `src/etl/extract/`.
    For example: `src/etl/extract/new_module/new_data.py`
2.  Update the configuration constants (`GSHEET_NAME`, `WORKSHEET_NAME`).
3.  Ensure the `CREDENTIALS_PATH` is correct.
"""

from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
from pipeline.utils.gsheet_to_pandas import gsheet_to_df

# --- CONFIGURATION ---
# TODO: Replace with the name of the Google Sheet file.
GSHEET_NAME = "Your-Google-Sheet-Name-Here"

# TODO: Replace with the exact name of the worksheet/tab to extract data from.
WORKSHEET_NAME = "Your-Worksheet-Name-Here"

# The path to the credentials file. This is typically kept in the project root.
CREDENTIALS_PATH = "credentials.json"


@task
def extract() -> Optional[pd.DataFrame]:
    """
    Extracts raw data from the specified Google Sheet worksheet.

    This function serves as the 'Extract' step in an ETL pipeline. It connects
    to the data source and returns the data as is, without transformation.

    Returns:
        A pandas DataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()
    logger.info(f"Extracting raw data from '{WORKSHEET_NAME}' in '{GSHEET_NAME}'...")

    # The gsheet_to_df function handles authentication, data fetching, and error handling.
    raw_df = gsheet_to_df(GSHEET_NAME, WORKSHEET_NAME, CREDENTIALS_PATH)

    if raw_df is None:
        logger.error("Failed to extract data. Aborting.")
        return None

    logger.info("Successfully extracted raw data.")
    return raw_df
