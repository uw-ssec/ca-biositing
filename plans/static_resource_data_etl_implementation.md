# Plan: Static Resource Data ETL Implementation

This plan outlines the steps to implement a new transform module for the
`static_resource_data` ETL pipeline, including LinkML schema updates and
corresponding tests.

## 1. Schema Management (LinkML)

### 1.1 New Entity: `LandiqResourceMapping`

- **Location:**
  [`resources/linkml/modules/external_data/landiq_resource_mapping.yaml`](resources/linkml/modules/external_data/landiq_resource_mapping.yaml)
- **Inheritance:** `BaseEntity`
- **Slots:**
  - `landiq_crop_name` (range: `string`): The crop name as it appears in LandIQ
    data.
  - `resource_id` (range: `Resource`): Foreign key to the `Resource` table.

### 1.2 Updates to `ResourceAvailability`

- **Location:**
  [`resources/linkml/modules/resource_information/resource_availability.yaml`](resources/linkml/modules/resource_information/resource_availability.yaml)
- **New Slots:**
  - `residue_factor_dry_tons_acre` (range: `float`): Dry tons per acre factor.
  - `residue_factor_wet_tons_acre` (range: `float`): Wet tons per acre factor.

### 1.3 Model & Migration Generation

- Execute:
  `pixi run update-schema -m "Add landiq_resource_mapping and residue factors to resource_availability"`
- This will:
  - Generate SQLAlchemy models in `ca_biositing.datamodels`.
  - Create a new Alembic migration script.

## 2. ETL Transform Module

### 2.1 Implementation

- **File:**
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/resource_information/static_resource_info.py`
- **Function:**
  `transform_static_resource_info(data_sources, etl_run_id, lineage_group_id)`
- **Dependencies:** `static_resource_info` (extracted from Google Sheets).

### 2.2 Transform Logic

1. **Cleaning & Coercion:**
   - Use `cleaning_mod.standard_clean` for column name normalization and
     whitespace stripping.
   - Use `coercion_mod.coerce_columns` to ensure `residue_factor_*` columns are
     floats.
2. **Normalization (ID Mapping):**
   - Use `normalize_dataframes` to map `resource` names to `resource_id`.
3. **Data Splitting:**
   - Create a DataFrame for `LandiqResourceMapping` records.
   - Create a DataFrame for `ResourceAvailability` records.
4. **Lineage Tracking:**
   - Assign `etl_run_id` and `lineage_group_id` to all records.

## 3. Testing Strategy

- **File:**
  `src/ca_biositing/pipeline/tests/test_static_resource_info_transform.py`
- **Tests:**
  - `test_transform_static_resource_info_success`: Verifies correct mapping of
    names to IDs and correct data types for residue factors.
  - `test_transform_static_resource_info_empty_input`: Ensures the module
    handles empty source data gracefully.
  - `test_transform_static_resource_info_missing_columns`: Validates behavior
    when expected columns are missing.

## 4. Execution Todo List

- [ ] Create
      `resources/linkml/modules/external_data/landiq_resource_mapping.yaml`
- [ ] Update
      `resources/linkml/modules/resource_information/resource_availability.yaml`
- [ ] Run `pixi run update-schema -m "Add landiq mapping and residue factors"`
- [ ] Create
      `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/resource_information/static_resource_info.py`
- [ ] Implement cleaning, coercion, and normalization logic
- [ ] Implement data splitting for LandIQ and Availability tables
- [ ] Create
      `src/ca_biositing/pipeline/tests/test_static_resource_info_transform.py`
- [ ] Run `pixi run migrate` to apply database changes
- [ ] Run `pixi run test` to verify the implementation
