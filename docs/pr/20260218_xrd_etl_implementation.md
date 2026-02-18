# XRD ETL Implementation Summary

This PR implements the ETL (Extract, Transform, Load) pipeline for XRD (X-ray
Diffraction) analysis data, following the established pattern for Aim 1
analytical records.

## Key Changes

### 1. New ETL Tasks

- **Transform**: Created
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/xrd_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/xrd_record.py)
  - Implements aggressive header cleaning (whitespace stripping, dropping empty
    columns, casing normalization).
  - Handles duplicate column de-duplication after normalization.
  - Performs normalization of foreign key fields (Resource, PreparedSample,
    etc.) using `normalize_dataframes`.
  - Maps XRD-specific fields: `scan_low_nm`, `scan_high_nm`.
- **Load**: Created
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/xrd_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/xrd_record.py)
  - Implements upsert logic based on `record_id`.

### 2. Flow Integration

- Updated
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/analysis_records.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/analysis_records.py)
  to include XRD extraction, transformation, and loading.
- Added XRD data to the global observation transformation step.
- Ensured `etl_run_id` and `lineage_group_id` are propagated through all steps.

### 3. Testing

- Added `test_xrd_etl_full` to
  [`src/ca_biositing/pipeline/tests/test_new_analysis_etl.py`](src/ca_biositing/pipeline/tests/test_new_analysis_etl.py)
  to verify the end-to-end extraction, transformation, and load mocking.

## Future Improvements

- **Raw Data URL Mapping**: Currently, `raw_data_url` mapping remains a future
  improvement across all analytical types.
