# Implementation Plan: Thermochemical Conversion ETL

This plan outlines the steps to implement the transformation and loading layers
for the Thermochemical Conversion ETL pipeline, following the established
patterns in the `ca-biositing` repository.

## Status: Final Implementation & Refinement Completed

The ETL pipeline for Thermochemical Conversion data is fully implemented and
operational. All initial requirements and subsequent refinements (including
observation fixes and model simplifications) have been addressed and verified
against the database.

## 1. Transformation Layer

### 1.1 `gasification_record.py`

**File Path:**
[`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/gasification_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/transform/analysis/gasification_record.py)

**Responsibilities:**

- Clean and coerce raw data from `02-ThermoData` and `01-ThermoExperiment` using
  `standard_clean`.
- Normalize entity names (Resource, PreparedSample, Method, Experiment, Contact,
  FileObjectMetadata) to database IDs using `normalize_dataframes`.
- Map relevant fields to the `GasificationRecord` SQLModel (record_id,
  technical_replicate_no, note, etc.).
- Ensure `record_id` is unique and mapped from the `Record_id` source column.

### 1.2 `observation.py` (Existing)

**Integration:**

- Uses the existing `transform_observation` task to process `02-ThermoData`.
- Fixed to correctly map `record_id` from source and ensure lowercase
  `record_type = 'gasification'`.
- Successfully populates the `observation` table with long-format parameter
  data.

## 2. Loading Layer

### 2.1 `gasification_record.py`

**File Path:**
[`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/gasification_record.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/etl/load/analysis/gasification_record.py)

**Responsibilities:**

- Implements `load_gasification_record(df: pd.DataFrame)` using the standard
  `UPSERT` pattern.
- Ensures data integrity and handles potential conflicts on `record_id`.

## 3. Orchestration (Prefect Flow)

### 3.1 `thermochem_etl.py`

**File Path:**
[`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/thermochem_etl.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/flows/thermochem_etl.py)

**Workflow Steps:**

1. **Initialize Lineage:** Create ETL run and lineage groups.
2. **Extract:** Call extractors from `thermochem_data.py`.
3. **Transform & Load Observations:** Analysis type is set to `'gasification'`
   and dataset to `'biocirv'`.
4. **Transform & Load Gasification Records:** Correctly passes lineage and
   metadata.
5. **Finalize:** Log completion status.

## 4. Completed Refinements

- [x] **Observation Population**: Fixed by mapping `Record_id` to `record_id`
      and improving name cleaning.
- [x] **Type & Dataset Mapping**: `analysis_type` is `'gasification'` and
      `dataset` is `'biocirv'`.
- [x] **Lineage Inheritance**: `GasificationRecord` correctly inherits
      `etl_run_id` and `lineage_group_id`.
- [x] **Record ID Mapping**: Now uses `Record_id` column from `thermo_data`.
- [x] **Replicate Mapping**: `Repl_no` -> `technical_replicate_no`.
- [x] **Raw Data Mapping**: `raw_data_url` normalized to `raw_data_id`.
- [x] **Note Mapping**: `Note` from source -> `note` in database.
- [x] **Model Simplification**: Removed `feedstock_mass`, `bed_temperature`, and
      `gas_flow_rate` from `GasificationRecord` model; these are now stored only
      as observations.

## 5. Verification Results

1. **Unit Tests:**
   `src/ca_biositing/pipeline/tests/test_thermochem_transform.py` validates all
   mappings.
2. **Database Verification:**
   - `SELECT record_type, COUNT(*) FROM observation GROUP BY record_type`
     confirms 459 'gasification' records.
   - `SELECT COUNT(*) FROM gasification_record` confirms 459 records with
     correct metadata.
