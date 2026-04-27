"""
Factory extractor for 01_Sample_IDs worksheet from SampleMetadata_v03-BioCirV.

This worksheet contains the primary sample identifiers and basic metadata:
- Sample_name: Unique sample identifier (join key across all four worksheets)
- Resource: Feedstock type (e.g., "Tomato pomace", "Olive pomace")
- ProviderCode: Provider identifier (maps to Provider.codename)
- FV_Date_Time: Collection timestamp (datetime format)
- Index: Unique row identifier
- FV_Folder: Google Drive folder link (for reference)

This extractor serves as the base for left-joining other worksheets.
"""

from .factory import create_extractor

GSHEET_NAME = "SampleMetadata_v03-BioCirV"
WORKSHEET_NAME = "01_Sample_IDs"

# Create the extract task using the factory pattern
extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME, task_name="extract_sample_ids")
