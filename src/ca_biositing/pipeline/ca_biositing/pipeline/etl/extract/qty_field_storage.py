"""
Factory extractor for 03_Qty_FieldStorage worksheet from SampleMetadata-BioCirV.

This worksheet contains sample quantity and field storage information:
- Sample_name: Unique sample identifier (join key)
- Resource, ProviderCode, FV_Date_Time: Redundant copies from 01_Sample_IDs
- Sample_Container: Container type and size (e.g., "Bucket (5 gal.)", "Core", "Bale")
  * Used for amount_collected_unit_id extraction (unit is embedded in this field)
- Qty: Amount collected (maps to amount_collected)
- Qty_Unit: Explicit unit column (if present; otherwise extract from Sample_Container)
- Primary_Collector: Collector identifier (maps to collector_id via Contact lookup)
- Collection_Team: Team members involved in collection
- Destination_Lab: Lab where sample was sent
- FieldStorage_Location: Storage location name (maps to field_storage_location_id)
- FieldStorage_Conditions: Storage conditions (temperature, humidity, etc.)
- FieldStorage_Duration: Duration stored in field
- Other metadata: Comments, dates, etc.

This extractor provides quantity, unit, and field storage context for collected samples.
"""

from .factory import create_extractor

GSHEET_NAME = "SampleMetadata-BioCirV"
WORKSHEET_NAME = "03_Qty_FieldStorage"

# Create the extract task using the factory pattern
extract = create_extractor(GSHEET_NAME, WORKSHEET_NAME, task_name="extract_qty_field_storage")
