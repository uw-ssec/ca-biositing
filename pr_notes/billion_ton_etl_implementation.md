# PR: Implementation of Billion Ton 2023 Agricultural ETL Pipeline

## Description

This PR implements a comprehensive ETL (Extract, Transform, Load) pipeline for
the **Billion Ton 2023 Agricultural Dataset**. The pipeline is designed to
process national agricultural residue data, filter for California-specific
records, and load them into the PostgreSQL database using optimized bulk
operations. It also includes schema enhancements to accommodate high-magnitude
energy content data and improved metadata association.

## Key Changes

### 1. Data Models & Schema Updates

- **`BillionTon2023Record` Schema Enhancement**:
  - Added `dataset_id` to the model to enable proper data lineage and filtering
    by source report.
  - Upgraded `production_energy_content` from `INTEGER` to `BIGINT` to prevent
    "numeric value out of range" errors when processing trillion-BTU data.
  - Updated relationships to include `Dataset` association.
- **Alembic Migrations**:
  - `4d125aa975fa_update_production_energy_content_to_bigint.py`: Handles the
    type migration for energy content.
  - `ab30129c589f_add_dataset_id_to_billionton2023record.py`: Adds the new
    dataset foreign key.

### 2. ETL Modules (`ca_biositing.pipeline`)

- **Extract**
  ([`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/extract/billion_ton.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/extract/billion_ton.py)):
  Implements robust local CSV reading with Prefect task integration and
  standardized logging.
- **Transform**
  ([`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/billion_ton.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/billion_ton.py)):
  - **Filtering**: Specifically targets California records.
  - **Cleaning**:
    - Normalized column names to `snake_case`.
    - **County Name Cleaning**: Automatically removes the " county" suffix
      (e.g., "Alameda County" -> "alameda") to align with project standards.
  - **GEOID Formatting**: Converts numeric FIPS codes to 5-digit string GEOIDs
    with leading zeros (e.g., `06001`).
  - **Normalization**: Uses `normalize_dataframes` to swap names for database
    IDs for `Resource`, `ResourceSubclass`, `Unit`, and `Dataset` ("billion ton
    2023 report").
- **Load**
  ([`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/billion_ton.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/billion_ton.py)):
  - **FK Integrity**: Dynamically ensures all referenced `Place` (county)
    records exist in the database before loading records, preventing Foreign Key
    violations.
  - **Bulk Insert**: Utilizes SQLAlchemy's optimized bulk insert for high
    performance.
  - **Type Casting**: Implements explicit integer casting to handle
    pandas-to-SQL type nuances.

### 3. Orchestration & Integration

- **Prefect Flow**
  ([`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/billion_ton_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/billion_ton_etl.py)):
  Orchestrates the full process with integrated lineage tracking (`EtlRun` and
  `LineageGroup`).
- **Flow Registration**: Added to `AVAILABLE_FLOWS` in
  [`resources/prefect/run_prefect_flow.py`](resources/prefect/run_prefect_flow.py)
  for master orchestration.

### 4. Quality Assurance

- **Unit Tests**
  ([`src/ca_biositing/pipeline/tests/test_billion_ton_etl.py`](src/ca_biositing/pipeline/tests/test_billion_ton_etl.py)):
  5 new comprehensive tests covering:
  - Successful extraction and error handling for missing files.
  - Transformation logic (California filtering, GEOID formatting, county name
    cleaning).
  - Load module verification (SQL session interaction and commit logic).

## Verification Results

- **Test Suite**: All 5 tests passed successfully (`pixi run pytest`).
- **End-to-End Execution**: Successfully processed the full dataset (105,786
  rows), filtering and loading 1,777 California records with all metadata and
  lineage fields correctly populated.

## Dependencies

- Requires `geoalchemy2` and `psycopg2` (included in the `etl` and `default`
  pixi environments).
