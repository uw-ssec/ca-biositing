"""
ETL Extract: Pretreatment Setup
---

This module extracts data from the '01.1-PretreatmentSetup' worksheet.
"""

from typing import Optional
import os
import pandas as pd
from prefect import task, get_run_logger
from ...utils.gsheet_to_pandas import gsheet_to_df

# --- CONFIGURATION ---
GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "01.1-PretreatmentSetup"
CREDENTIALS_PATH = "credentials.json"


@task
def extract(project_root: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Extracts raw data from the specified Google Sheet worksheet.
    """
    logger = get_run_logger()
    logger.info(f"Extracting raw data from '{WORKSHEET_NAME}' in '{GSHEET_NAME}'...")

    credentials_path = CREDENTIALS_PATH
    if project_root:
        credentials_path = os.path.join(project_root, CREDENTIALS_PATH)

    raw_df = gsheet_to_df(GSHEET_NAME, WORKSHEET_NAME, credentials_path)

    if raw_df is None:
        logger.error("Failed to extract data. Aborting.")
        return None

    logger.info("Successfully extracted raw data.")
    return raw_df
