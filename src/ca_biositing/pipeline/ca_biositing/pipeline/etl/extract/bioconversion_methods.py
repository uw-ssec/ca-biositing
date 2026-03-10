"""
ETL Extract: BioConversion Methods
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "03.3-BioConversionMethods"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
