"""
ETL Extract: Resource Images
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "08.0_Resource_images"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
