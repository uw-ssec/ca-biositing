"""
ETL Extract: Resources
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "07.2-Resources"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
