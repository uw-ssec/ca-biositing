# PR Summary: Fix Analysis API Blocking due to empty `location_address` table

## Overview

The analysis API endpoints (`/v1/feedstocks/analysis/...`) were returning zero
results because the join chain required a valid mapping through the
`location_address` table. Since `location_address` was empty, all `INNER JOIN`
operations on sampling locations were failing.

This PR implements a new ETL sub-process for the `location_address` table and
integrates it into the existing `Field Sample ETL` flow.

## Changes

### 1. New ETL Components

- **`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/field_sampling/location_address.py`**:
  - Extracts unique location metadata (sampling location, city, street, zip)
    from the `samplemetadata` Google Sheet.
- **`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/location_address.py`**:
  - Maps these locations to the correct `geography_id` from the `place` table.
  - Implements a fallback to the California state geoid (`06000`) for generic or
    unmapped locations.
  - Implements an idempotent loader that upserts location records into the
    `location_address` table.

### 2. ETL Flow Integration

- **`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/field_sample_etl.py`**:
  - Modified the flow to execute `transform_location_address` and
    `load_location_address` _before_ the `field_sample` step.
  - This ensures that when `field_sample` records are created, they can
    correctly link to an existing `location_address.id`.

### 3. Field Sample Linkage

- **`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/field_sampling/field_sample.py`**:
  - Refactored to preserve location metadata during transformation.
- **`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/field_sample.py`**:
  - Now handles the linkage to `location_address` during the load phase,
    ensuring no database connection is required during transformation.

### 4. CI/CD & Build Fixes

- **Test Stability**: Separated DB lookups from transform tasks to allow unit
  tests to run with mocks and no live database connection.
- **Dependency Management**: Standardized engine usage to `get_engine()` across
  load tasks to ensure compatibility with existing test suites.
- **Build Configuration**: Updated `pyproject.toml` files for all packages to
  use explicit `packages` discovery, resolving wheel build errors related to
  duplicate `__init__.py` files in namespace packages.

## Verification

- **Test Suite**: Confirmed all 36 pipeline tests pass locally
  (`pixi run pytest src/ca_biositing/pipeline/tests/`).
- **Database Status**: Confirmed `location_address` table is now populated with
  unique entries.
- **Data Integrity**: Verified that `field_sample` records are correctly linked
  to location entries with valid geography IDs.
- **API Impact**: The join chain in `AnalysisService` is no longer returning
  zero rows, unblocking the analysis endpoints.

## Related Issues

- Unblocks API endpoint:
  `GET /v1/feedstocks/analysis/resources/{resource}/geoid/{geoid}/parameters`
