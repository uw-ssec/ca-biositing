"""
ETL Extract: County Ag Reports
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"

primary_products = create_extractor(GSHEET_NAME, "07.7-Primary_products")
pp_production_value = create_extractor(GSHEET_NAME, "07.7a-PP_Prodn_Value")
pp_data_sources = create_extractor(GSHEET_NAME, "07.7b-PP_Data_sources")
