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

    @task(
        name=task_name or f"extract_{worksheet_name.lower().replace('.', '_').replace('-', '_')}",
        retries=3,
        retry_delay_seconds=10
    )
    def extract(project_root: Optional[str] = None) -> pd.DataFrame:
        from ca_biositing.pipeline.utils.gsheet_to_pandas import gsheet_to_df
        logger = get_run_logger()
        logger.info(f"Extracting raw data from '{worksheet_name}' in '{gsheet_name}'...")

        credentials_path = os.getenv("CREDENTIALS_PATH", "credentials.json")
        if project_root:
            credentials_path = os.path.join(project_root, credentials_path)

        try:
            raw_df = gsheet_to_df(gsheet_name, worksheet_name, credentials_path)
        except Exception as e:
            msg = f"Failed to extract data from {gsheet_name}/{worksheet_name}: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e

        if raw_df is None:
            msg = f"Extractor returned None for {gsheet_name}/{worksheet_name}. Aborting."
            logger.error(msg)
            raise RuntimeError(msg)

        logger.info(f"Successfully extracted raw data from {worksheet_name}.")
        return raw_df

    return extract
