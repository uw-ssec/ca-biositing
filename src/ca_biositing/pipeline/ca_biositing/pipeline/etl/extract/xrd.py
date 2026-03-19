"""
ETL Extract: XRD
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "03.4-XRD"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
