"""
ETL Extract: Compost
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "01.4-Compost"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
