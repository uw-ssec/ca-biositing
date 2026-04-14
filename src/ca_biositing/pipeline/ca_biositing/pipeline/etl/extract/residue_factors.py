"""
ETL Extract: Residue Factors

Extracts residue factor data from Google Sheets using the factory pattern.
Returns raw DataFrame with all columns from the "Data_Views" worksheet.
"""

from .factory import create_extractor

# Configuration
GSHEET_NAME = "Residue Factors"
WORKSHEET_NAME = "Data_Views"

# Create extractor task using factory pattern
extract_residue_factors = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
