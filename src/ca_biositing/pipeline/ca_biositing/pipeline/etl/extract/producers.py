"""
Factory extractor for 04_Producers worksheet from SampleMetadata_v03-BioCirV.

This worksheet contains producer/origin information and extended sample metadata:
- Sample_name: Unique sample identifier (join key)
- Resource, ProviderCode, FV_Date_Time: Redundant copies from 01_Sample_IDs
- Producer: Producer name (identifies the source organization)
- Prod_Location: Producer location name (maps to field_sample_storage_location_id)
- Prod_Street, Prod_City, Prod_Zip: Producer address components
- Prod_Date: Production date
- Harvest_Method: Method used for harvesting
- Treatment: Treatment applied to the sample
- Soil_Type: Type of soil at production location
- Crop_Variety, Crop_Cultivar: Variety and cultivar information
- Production_Notes: Notes about the production process
- Other metadata: Additional extended fields for sample context

This extractor provides producer/origin context and addresses for
field_sample_storage_location_id creation via LocationAddress.
"""

from .factory import create_extractor

GSHEET_NAME = "SampleMetadata_v03-BioCirV"
WORKSHEET_NAME = "04_Producers"

# Create the extract task using the factory pattern
extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME, task_name="extract_producers")
