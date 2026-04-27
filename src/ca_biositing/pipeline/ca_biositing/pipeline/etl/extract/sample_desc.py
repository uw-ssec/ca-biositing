"""
Factory extractor for 02_Sample_Desc worksheet from SampleMetadata_v03-BioCirV.

This worksheet contains detailed sample description and location information:
- Sample_name: Unique sample identifier (join key)
- Resource, ProviderCode, FV_Date_Time: Redundant copies from 01_Sample_IDs
- Sampling_Location, Sampling_Street, Sampling_City, Sampling_Zip, Sampling_LatLong:
  Collection location details
- Sample_TS: Sample timestamp
- Sample_Source: Sample source classification
- Processing_Method: Processing method (maps to new Methods column, not collection_method_id)
- Storage_Mode, Storage_Dur_Value, Storage_Dur_Units: Field storage details
- Particle_L_cm, Particle_W_cm, Particle_H_cm: Extended particle dimensions
- Sample_Notes: Notes about the sample

Currently sparse (many empty fields) but provides spatial and descriptive context.
"""

from .factory import create_extractor

GSHEET_NAME = "SampleMetadata_v03-BioCirV"
WORKSHEET_NAME = "02_Sample_Desc"

# Create the extract task using the factory pattern
extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME, task_name="extract_sample_desc")
