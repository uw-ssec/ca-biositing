"""
ETL Extract: BioConversion Setup
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "01.2-BioConversionSetup"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
