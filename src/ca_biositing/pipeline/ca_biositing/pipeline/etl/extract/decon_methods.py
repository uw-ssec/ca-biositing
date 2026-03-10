"""
ETL Extract: Decon Methods
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "03.1-DeconMethods"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
