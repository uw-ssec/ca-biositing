# PR: Prepared Sample ETL Implementation and Samples Orchestration

## Overview

This PR implements the ETL pipeline for the `prepared_sample` table and
introduces a unified `samples` orchestration flow that manages both field and
prepared samples.

## Key Components

### 1. Prepared Sample ETL

The `prepared_sample` ETL pipeline processes feedstock preparation data from
Google Sheets into the PostgreSQL database.

- **Extract**: Pulls raw data from the "02-Preparation" worksheet of the "Aim
  1-Feedstock Collection and Processing Data-BioCirV" Google Sheet.
- **Transform**:
  - Standardizes column names to snake_case.
  - Coerces data types (numeric, datetime, boolean).
  - Performs name-to-ID swapping for `field_sample_id`, `prep_method_id`, and
    `preparer_id` using database lookups.
  - Implements lineage tracking.
- **Load**: Performs upserts into the `prepared_sample` table based on the
  unique `name` column.

### 2. Testing

Comprehensive tests were implemented to ensure data integrity:

- **Transform Tests**:
  [`src/ca_biositing/pipeline/tests/test_prepared_sample_transform.py`](src/ca_biositing/pipeline/tests/test_prepared_sample_transform.py)
  verifies cleaning logic and ID mapping.
- **Load Tests**:
  [`src/ca_biositing/pipeline/tests/test_prepared_sample_load.py`](src/ca_biositing/pipeline/tests/test_prepared_sample_load.py)
  verifies database upsert behavior.

### 3. Flow Orchestration

Two new Prefect flows were created:

- **`prepared_sample_etl_flow`**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/prepared_sample_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/prepared_sample_etl.py) -
  The standalone flow for preparation data.
- **`samples_etl_flow`**:
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/samples_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/samples_etl.py) -
  A parent flow that orchestrates:
  1. `field_sample_etl_flow`
  2. `prepared_sample_etl_flow`

This ensures that field samples (the parent records) are always processed before
prepared samples (the child records).

### 4. Registration

The flows have been registered in
[`resources/prefect/run_prefect_flow.py`](resources/prefect/run_prefect_flow.py).

- The individual `field_sample` and `prepared_sample` flows are now commented
  out in the registry.
- The unified `samples` flow is active, serving as the single entry point for
  all sampling data.

## How to Run

To run the combined sampling pipeline:

```bash
pixi run python -c 'from ca_biositing.pipeline.flows.samples_etl import samples_etl_flow; samples_etl_flow()'
```

Or via the master flow:

```bash
# Inside the container
prefect deploy
```
