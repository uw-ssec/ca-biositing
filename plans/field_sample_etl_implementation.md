# Field Sample ETL Implementation Plan

This plan outlines the steps to implement the load module, tests, and Prefect
flow for the `field_sample` table.

## 1. Load Module Implementation

- **File**:
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/field_sample.py`
- **Task**: `load_field_sample(df: pd.DataFrame)`
- **Logic**:
  - Use `get_local_engine()` for database connectivity.
  - Implement a name-based upsert logic using pandas and SQLAlchemy.
  - For each row in the DataFrame:
    - Check if a record with the same `name` exists in the `field_sample` table.
    - If it exists, update the existing record with the new values.
    - If it does not exist, create a new record.
  - Ensure `created_at` and `updated_at` timestamps are handled correctly.
  - Use lazy imports for models to avoid Docker import hangs.

## 2. Test Implementation

- **File**: `src/ca_biositing/pipeline/tests/test_field_sample_load.py`
- **Tests**:
  - `test_load_field_sample_insert`: Verify that new records are inserted
    correctly.
  - `test_load_field_sample_update`: Verify that existing records are updated
    based on the `name` column.
- **Setup**: Use the existing `session` and `engine` fixtures.

## 3. Prefect Flow Registration

- **File**:
  `src/ca_biositing/pipeline/ca_biositing/pipeline/flows/field_sample_etl.py`
- **Flow**: `field_sample_etl_flow()`
- **Steps**:
  - Call `extract_basic_sample_info` (and other required sources).
  - Call `transform_field_sample`.
  - Call `load_field_sample`.
- **Lineage**: Ensure `etl_run_id` and `lineage_group_id` are passed through the
  flow.

## 4. Verification

- Run the new tests using
  `pixi run test src/ca_biositing/pipeline/tests/test_field_sample_load.py`.
- Verify the flow can be loaded by Prefect.
