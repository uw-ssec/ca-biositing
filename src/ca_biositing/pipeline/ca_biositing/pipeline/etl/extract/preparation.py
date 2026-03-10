"""
ETL Extract: Preparation
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "02-Preparation"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
