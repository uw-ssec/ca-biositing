"""
ETL Extract: Autoclave
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "01.3-Autoclave"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
