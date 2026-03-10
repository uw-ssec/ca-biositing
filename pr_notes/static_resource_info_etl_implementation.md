# PR Summary: Static Resource Information ETL Implementation

## Overview

This PR implements a new ETL pipeline for processing static resource information
from Google Sheets into the PostgreSQL database. This includes mapping LandIQ
crop names to internal resource IDs and providing residue yield factors (wet/dry
tons per acre) for those resources.

## Key Changes

### 1. Schema Updates (LinkML)

- **New Module**: Created
  `resources/linkml/modules/external_data/landiq_resource_mapping.yaml` to
  define the mapping between LandIQ crop names and internal resources.
- **Updated Module**: Enhanced
  `resources/linkml/modules/resource_information/resource_availability.yaml`
  with new slots:
  - `residue_factor_dry_tons_acre`
  - `residue_factor_wet_tons_acre`
- **Database Migrations**: Generated and applied SQLAlchemy models and Alembic
  migrations to reflect these schema changes.

### 2. ETL Pipeline Implementation

- **Extract**: Implemented
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/extract/static_resource_info.py`
  to fetch data from the "static_resource_info" worksheet in the
  "Static_resource_information" Google Sheet.
- **Transform**: Implemented
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/resource_information/static_resource_info.py`.
  - Performs standard cleaning and name normalization.
  - Coerces residue factors to numeric types.
  - Maps resource names and LandIQ crop names to their respective database IDs
    using `normalize_dataframes`.
  - Splits data into `LandiqResourceMapping` and `ResourceAvailability` records.
- **Load**: Implemented
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/static_resource_info.py`.
  - Handles upsert logic for both mapping and availability tables.
  - Ensures data integrity by checking for existing records based on unique
    constraints.
- **Flow**: Created
  `src/ca_biositing/pipeline/ca_biositing/pipeline/flows/static_resource_info.py`
  to orchestrate the ETL process using Prefect, including lineage tracking.

### 3. Testing

- Added comprehensive tests for the ETL process:
  - `src/ca_biositing/pipeline/tests/test_static_resource_info_extract.py`
  - `src/ca_biositing/pipeline/tests/test_static_resource_info_transform.py`
  - `src/ca_biositing/pipeline/tests/test_static_resource_info_load.py`
- Verified successful flow execution and data persistence.

## Verification Results

- `pixi run update-schema`: Successful.
- `pixi run migrate`: Successful.
- `pixi run test`: All tests passing.
- Prefect Flow: Registered and executed successfully.
