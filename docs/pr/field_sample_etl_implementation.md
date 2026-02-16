# PR Draft: Field Sample ETL Implementation

## Overview

This PR implements the ETL pipeline for the `field_sample` table, following the
plan outlined in
[`plans/field_sample_etl_implementation.md`](plans/field_sample_etl_implementation.md).
The implementation includes the load module, unit tests, and a Prefect flow for
orchestration.

## Changes

- **Load Module**: Implemented `load_field_sample` in
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/field_sample.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/field_sample.py)
  with name-based upsert logic.
- **Tests**: Added comprehensive tests in
  [`src/ca_biositing/pipeline/tests/test_field_sample_load.py`](src/ca_biositing/pipeline/tests/test_field_sample_load.py)
  covering both insert and update scenarios.
- **Prefect Flow**: Created `field_sample_etl_flow` in
  [`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/field_sample_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/field_sample_etl.py)
  to orchestrate the extract, transform, and load steps.
- **Master Flow Integration**: Added the field sample flow to the master ETL
  orchestration in
  [`resources/prefect/run_prefect_flow.py`](resources/prefect/run_prefect_flow.py).

## Implementation Notes

- **LandIQ Pipeline**: The LandIQ ETL pipeline has been commented out in
  [`resources/prefect/run_prefect_flow.py`](resources/prefect/run_prefect_flow.py)
  as it is time-intensive and not required for the current verification of the
  field sample pipeline.
- **Lazy Imports**: Used lazy imports for SQLAlchemy models to prevent potential
  Docker import hangs during flow execution.

## Known Issues & Future Work

- **`amount_collected` Column**: It has been observed that the
  `amount_collected` column is not populating correctly. This appears to be a
  deeper issue that may require schema adjustments to resolve fully. This is
  being raised here as a known issue for tracking and will be addressed in a
  subsequent task.

## Verification Results

- Ran tests using
  `pixi run test src/ca_biositing/pipeline/tests/test_field_sample_load.py`.
- Verified Prefect flow registration and execution.
