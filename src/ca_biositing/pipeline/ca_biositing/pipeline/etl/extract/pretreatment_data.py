"""
ETL Extract: Pretreatment Data
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Biomass Biochem Conversion Data-BioCirV"
WORKSHEET_NAME = "02.1-PretreatmentData"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
