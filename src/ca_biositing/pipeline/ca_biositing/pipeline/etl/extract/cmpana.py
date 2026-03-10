"""
ETL Extract: CmpAna
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"
WORKSHEET_NAME = "03.3-CmpAna"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
