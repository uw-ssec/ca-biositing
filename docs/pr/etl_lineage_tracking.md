# PR Summary: ETL Lineage Tracking Implementation

## Overview

This PR implements a robust ETL lineage tracking system across the primary
analysis modules. It enables end-to-end traceability by linking every database
record to its specific Prefect pipeline execution.

## Key Changes

### 1. Schema & Data Model

- **LinkML Updates**:
  - Added `run_id` (string) to the `EtlRun` model to store external identifiers
    (e.g., Prefect UUIDs).
  - Standardized `etl_run_id` as an `Integer` foreign key across all entities
    via `BaseEntity`.
- **Database Migration**:
  - Generated and applied a migration to update existing tables.
  - Included custom `USING` clauses in the migration to safely convert existing
    `TEXT` lineage columns to `INTEGER`.

### 2. Lineage Utilities

- Created `ca_biositing.pipeline.utils.lineage`:
  - `create_etl_run_record`: Captures Prefect context, stores the UUID in
    `run_id`, and returns a stable database `id`.
  - `create_lineage_group`: Allows grouping of related records within a single
    run.

### 3. ETL Pipeline Integration

- **Modules Updated**: `proximate_record`, `ultimate_record`,
  `compositional_record`, and `observation`.
- **Transformation**: Tasks now accept `etl_run_id` and `lineage_group_id`. IDs
  are injected _after_ standard cleaning to ensure data integrity.
- **Loading**: Upsert logic now correctly handles lineage columns, ensuring
  metadata is updated or preserved as intended.
- **Orchestration**: The `analysis_records_flow` now initializes lineage
  tracking at the start of execution and propagates IDs to all sub-tasks.

## Verification Results

- `EtlRun` table correctly populates with Prefect UUIDs and auto-incrementing
  IDs.
- Analysis tables (`proximate_record`, etc.) now contain valid integer foreign
  keys pointing to the corresponding `etl_run`.
- Verified that lineage information is preserved/updated correctly during
  database upserts.
