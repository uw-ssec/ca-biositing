# PR: ICP, XRF, and Calorimetry ETL Implementation

## Description

This PR implements the Extract, Transform, and Load (ETL) pipelines for three
new analytical datasets: **ICP**, **XRF**, and **Calorimetry**. These pipelines
are integrated into the existing `analysis_records` flow, which now handles a
total of six analytical record types.

The implementation follows the established pattern for `ProximateRecord`,
ensuring consistent data processing, lineage tracking, and database integration
across all Aim 1 analytical records.

## Key Changes

### 1. New Transform Modules

Created specialized transformation logic for each new analysis type in
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/`:

- `icp_record.py`: Handles elemental analysis data.
- `xrf_record.py`: Handles X-ray fluorescence data, including specific fields
  for `wavelength_nm`, `intensity`, `energy_slope`, and `energy_offset`.
- `calorimetry_record.py`: Handles high heating value (HHV) and other caloric
  data.

### 2. New Load Modules

Implemented upsert logic for the new database tables in
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/`:

- `icp_record.py`, `xrf_record.py`, and `calorimetry_record.py` now support safe
  database loading with conflict handling.

### 3. Flow Integration

Updated the `Analysis Records ETL` flow in
`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/analysis_records.py`:

- Integrated extractors, transformers, and loaders for all three new types.
- Maintained unified lineage tracking across the entire analytical suite.
- Aggregated observations from all six record types into the global
  `Observation` table.

### 4. Robustness and Data Quality Improvements

During implementation, several data quality issues in the raw Google Sheets were
identified and addressed via enhanced transformation logic:

- **Header Cleaning**: Added automatic whitespace stripping from all column
  headers.
- **Empty Column Handling**: Automatically identifies and drops "ghost" empty
  columns often found at the end of Excel/Google Sheet exports.
- **De-duplication**: Implemented a robust multi-step de-duplication process.
  The transformer now cleans names _before_ checking for duplicates, ensuring
  that columns which normalize to the same name (e.g., 'Upload Status' and
  'Upload_status') are merged correctly. This fixes a common crash in the
  `to_lowercase_df` utility.

## Testing

- Created a new test suite:
  `src/ca_biositing/pipeline/tests/test_new_analysis_etl.py`.
- Verified full ETL cycles (Extract -> Transform -> Load) using mocks for
  external services.
- Successfully validated the flow with a production run against live Google
  Sheets.

## Limitations & Future Improvements

- **Data URL Mapping**: Currently, fields such as `raw_data_url` (present in
  ICP, Ultimate, and Compositional tabs) and `spectral_data_url` (present in the
  XRF tab) are not being populated in the database.
- **Recommendation**: Future iterations should implement logic to map these URLs
  to the `raw_data_id` field (linking to the `file_object_metadata` table) to
  enable direct traceability to raw data sources.

## Deployment Notes

- To pick up the latest transformation logic in Docker environments, a service
  rebuild is recommended:
  ```bash
  pixi run rebuild-services
  ```
