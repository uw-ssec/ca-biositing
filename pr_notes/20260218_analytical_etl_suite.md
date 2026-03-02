# PR: Comprehensive Analytical Suite ETL Implementation (ICP, XRF, Calorimetry, XRD)

## Description

This PR implements the Extract, Transform, and Load (ETL) pipelines for four new
analytical datasets: **ICP**, **XRF**, **Calorimetry**, and **XRD**. These
pipelines are integrated into the existing `analysis_records` flow, which now
handles a total of seven analytical record types (including the original
Proximate, Ultimate, and Compositional).

The implementation ensures consistent data processing, lineage tracking, and
database integration across all Aim 1 analytical records.

## Key Changes

### 1. New Transform Modules

Created specialized transformation logic in
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/`:

- `icp_record.py`: Elemental analysis data.
- `xrf_record.py`: X-ray fluorescence data (wavelength, intensity, energy
  slope/offset).
- `calorimetry_record.py`: High heating value (HHV) and caloric data.
- `xrd_record.py`: X-ray diffraction data (scan ranges).

### 2. New Load Modules

Implemented upsert logic (on-conflict update) in
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/`:

- Support for `icp_record`, `xrf_record`, `calorimetry_record`, and `xrd_record`
  tables.

### 3. Flow Integration

Updated the `Analysis Records ETL` flow in
`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/analysis_records.py`:

- Integrated all four new analysis types.
- Unified lineage tracking (ETL Run ID and Lineage Group ID) across the suite.
- Aggregated observations from all seven record types into the global
  `Observation` table.

### 4. Robustness and Data Quality Improvements

- **Header Cleaning**: Automatic whitespace stripping and "ghost" column
  removal.
- **Advanced De-duplication**: Normalizes column names _before_ de-duplication
  to prevent crashes caused by case variations (e.g., 'Upload Status' vs
  'upload_status').
- **Lineage Consistency**: Guaranteed propagation of ETL metadata through all
  transformation steps.
- **Raw Data URL Mapping**: Implemented automated mapping of Google Drive/Sheet
  URLs to the `file_object_metadata` table. Analytical records are now linked
  via the `raw_data_id` foreign key, enabling full traceability from database
  records back to raw source files.

## Testing

- Suite: `src/ca_biositing/pipeline/tests/test_new_analysis_etl.py`.
- Verified full ETL cycles (Extract -> Transform -> Load) for all new types
  using mocks, including verification of `raw_data_id` population.
- Validated against live Google Sheet data, confirming successful linking for
  ICP and XRF records.

## Limitations & Future Improvements

- **Multiple URLs**: For records with multiple associated URLs (e.g., XRF
  spectral data), the system currently prioritizes mapping the primary URL to
  `raw_data_id`.
