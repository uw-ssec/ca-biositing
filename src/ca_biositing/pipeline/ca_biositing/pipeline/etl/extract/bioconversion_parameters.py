"""
ETL Extract: BioConv Parameters
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "03.4-BioConvParameters"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
