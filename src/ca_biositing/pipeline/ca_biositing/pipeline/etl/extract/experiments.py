"""
ETL Extract: Experiments
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "03.0-Experiments"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME, task_name="extract_experiments")
