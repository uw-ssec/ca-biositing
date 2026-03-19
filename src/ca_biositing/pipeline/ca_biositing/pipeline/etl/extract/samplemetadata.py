"""
ETL Extract: SampleMetadata
"""

from .factory import create_extractor

GSHEET_NAME = "Sampling_data_redacted"
WORKSHEET_NAME = "samplemetadata"

extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME)
