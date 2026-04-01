# Handoff: Thermochemical Conversion ETL

This document provides instructions for running the Thermochemical Conversion
ETL pipeline and maintaining its test suite.

## 1. Pipeline Overview

The pipeline extracts data from the "Aim 2-Thermochem Conversion Data-BioCirV"
Google Sheet and loads it into the `observation` and `gasification_record`
tables.

### Key Files

- **Flow**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/thermochem_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/thermochem_etl.py)
- **Transform (Gasification)**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/gasification_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/gasification_record.py)
- **Transform (Observation)**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/observation.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/observation.py)
- **Load**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/gasification_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/gasification_record.py)
- **Model**:
  [`src/ca_biositing/datamodels/ca_biositing/datamodels/models/aim2_records/gasification_record.py`](src/ca_biositing/datamodels/ca_biositing/datamodels/models/aim2_records/gasification_record.py)

## 2. Running the ETL

The pipeline is registered in the master flow runner. You can run it via Pixi:

```bash
# Start services (DB and Prefect)
pixi run start-services

# Run the Master ETL Flow (which includes Thermochem)
pixi run run-etl
```

Alternatively, run the flow script directly:

```bash
cd src/ca_biositing/pipeline
pixi run python ca_biositing/pipeline/flows/thermochem_etl.py
```

## 3. Running & Updating Tests

### Running Tests

The tests are located in `src/ca_biositing/pipeline/tests/`.

```bash
cd src/ca_biositing/pipeline
# Run all thermochem related tests
pixi run pytest tests/test_thermochem_extract.py tests/test_thermochem_transform.py --verbose
```

### Updating `test_thermochem_transform.py`

The transformation tests currently fail because they reflect the initial
"long-to-wide" logic which was removed in favor of a simpler observation-based
approach.

To update the tests:

1.  **Update Mock Data**: Use `record_id` instead of `Rx_UUID` in the mock
    DataFrames.
2.  **Update Assertions**:
    - Remove checks for `feedstock_mass`, `bed_temperature`, and
      `gas_flow_rate`.
    - Add checks for `technical_replicate_no` (mapped from `Repl_no`).
    - Verify that `record_id` is correctly lowercased by the `standard_clean`
      process.
3.  **Check Normalization**: Ensure `raw_data_url` is included in the
    normalization columns to verify `raw_data_id` resolution.

## 4. Database Verification

To verify the data load manually:

```bash
# Check observation counts by type
pixi run access-db -c "SELECT record_type, COUNT(*) FROM observation GROUP BY record_type"

# Verify gasification records
pixi run access-db -c "SELECT COUNT(*) FROM gasification_record"
```

## 5. Current Status

- Observations: **459 records** successfully loaded.
- Gasification Records: **459 records** successfully loaded.
- Type: `gasification` (lowercase).
- Dataset: `biocirv` (lowercase).
- Lineage: Fully tracked via `etl_run_id` and `lineage_group_id`.
