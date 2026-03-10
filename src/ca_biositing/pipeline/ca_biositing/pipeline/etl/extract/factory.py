"""
Extractor Factory for GSheet-based ETL tasks.
"""

from typing import Optional
import os
import pandas as pd
from prefect import task, get_run_logger

def create_extractor(gsheet_name: str, worksheet_name: str, task_name: Optional[str] = None):
    """
    Creates a Prefect task for extracting data from a specific GSheet worksheet.
    """

    @task(name=task_name or f"extract_{worksheet_name.lower().replace('.', '_').replace('-', '_')}")
    def extract(project_root: Optional[str] = None) -> Optional[pd.DataFrame]:
        from ca_biositing.pipeline.utils.gsheet_to_pandas import gsheet_to_df
        logger = get_run_logger()
        logger.info(f"Extracting raw data from '{worksheet_name}' in '{gsheet_name}'...")

        credentials_path = os.getenv("CREDENTIALS_PATH", "credentials.json")
        if project_root:
            credentials_path = os.path.join(project_root, credentials_path)

        raw_df = gsheet_to_df(gsheet_name, worksheet_name, credentials_path)

        if raw_df is None:
            logger.error(f"Failed to extract data from {worksheet_name}. Aborting.")
            return None

        logger.info(f"Successfully extracted raw data from {worksheet_name}.")
        return raw_df

    return extract
