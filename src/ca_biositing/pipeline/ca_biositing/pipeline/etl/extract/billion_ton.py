from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
import os
import tempfile

@task
def extract(
    file_id: str = "11xLy_kPTHvoqciUMy3SYA3DLCDIjkOGa",
    file_name: str = "billionton_23_agri_download.csv",
    mime_type: str = "text/csv",
    project_root: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """
    Extracts raw Billion Ton data from a file on Google Drive.

    Args:
        file_id: The Google Drive File ID.
        file_name: The local filename to save as.
        mime_type: The MIME type of the file.
        project_root: Optional root directory of the project.

    Returns:
        A pandas DataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()

    CREDENTIALS_PATH = "credentials.json"

    logger.info(f"Extracting raw data from Google Drive ID: '{file_id}'...")

    # Set up paths
    credentials_path = CREDENTIALS_PATH
    if project_root:
        credentials_path = os.path.join(project_root, CREDENTIALS_PATH)

    # Use a temporary directory for the download to avoid hardcoding paths
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.info(f"Using temporary directory for download: {temp_dir}")

        try:
            from ca_biositing.pipeline.utils.gdrive_to_pandas import gdrive_to_df
            # Use the gdrive_to_df utility to fetch and load the data
            raw_df = gdrive_to_df(
                file_name=file_name,
                mime_type=mime_type,
                credentials_path=credentials_path,
                dataset_folder=temp_dir,
                file_id=file_id
            )

            if raw_df is None or raw_df.empty:
                logger.error(f"Failed to extract data from Google Drive ID '{file_id}'.")
                return None

            logger.info(f"Successfully extracted {len(raw_df)} rows from Google Drive.")
            return raw_df
        except Exception:
            logger.exception("An error occurred during extraction from Google Drive")
            return None
