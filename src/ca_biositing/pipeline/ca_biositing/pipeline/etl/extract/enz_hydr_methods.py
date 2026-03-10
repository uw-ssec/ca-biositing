"""
ETL Extract: Enz Hydr Methods
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "03.2-EnzHydrMethods"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
