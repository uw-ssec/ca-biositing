"""
ETL Extract: Thermochemical Conversion Data
"""

from .factory import create_extractor

GSHEET_NAME = "Aim 2-Thermochem Conversion Data-BioCirV"

# Experiment & Data
thermo_experiment = create_extractor(GSHEET_NAME, "01-ThermoExperiment")
thermo_data = create_extractor(GSHEET_NAME, "02-ThermoData")

# Setup & Infrastructure
reaction_setup = create_extractor(GSHEET_NAME, "01.2-ReactionSetup")
thermo_methods = create_extractor(GSHEET_NAME, "03-ThermoMethods")
thermo_reactors = create_extractor(GSHEET_NAME, "04-ThermoReactors")
thermo_parameters = create_extractor(GSHEET_NAME, "05-ThermoParameters")

# Reference Sheets (Aim 1 integration)
aim1_material_types = create_extractor(GSHEET_NAME, "06-Aim1-Material_Types")
aim1_preprocessing = create_extractor(GSHEET_NAME, "07-Aim1-Preprocessing")

# Metadata/Readme (optional, but included for completeness)
readme = create_extractor(GSHEET_NAME, "00-Aim2-readme")
sheet_improvements = create_extractor(GSHEET_NAME, "00-Aim2-SheetImprovements")
