# PR: Land IQ Pipeline Enhancements and Performance Optimization

## Overview

This PR delivers significant enhancements to the Land IQ ETL pipeline, focusing
on data richness, schema robustness, and high-performance bulk loading. It
addresses the requirements for capturing crop percentage data and implements the
optimizations outlined in the `landiq_optimization_plan.md`.

## Key Changes

### 1. Data Richness: Crop Percentages & Dataset Versioning

- **New Columns**: Added `pct1`, `pct2`, `pct3`, and `pct4` to the
  `LandiqRecord` model to capture the percentage of each crop type on a field.
- **Numeric Coercion**: Implemented robust transformation logic to handle
  non-numeric values (e.g., `**`) in the source shapefile, ensuring they are
  correctly coerced to numeric types or nulls.
- **Dataset Association**: All records and polygons are now explicitly
  associated with the `landiq_2023` dataset, enabling multi-year data
  versioning.

### 2. Performance Optimization (Bulk Loading)

- **Bulk ID Resolution**: Replaced the row-by-row "check-then-upsert" pattern
  with a high-performance bulk strategy.
- **Polygon "Insert-Ignore"**: Implemented `bulk_insert_polygons_ignore` using
  PostgreSQL's `ON CONFLICT DO NOTHING` with a functional index on `md5(geom)`.
- **In-Memory Mapping**: Resolved IDs for Polygons, Crops, and Datasets in bulk,
  performing normalization in Python memory to eliminate thousands of database
  round-trips.
- **Bulk Upsert**: Refactored `load_landiq_record` to use
  `ON CONFLICT (record_id) DO UPDATE`, collapsing ingestion time for large
  chunks.

### 3. Schema & Migration Improvements

- **Composite Unique Keys**: Updated the `Polygon` model to use a composite
  unique constraint on `(md5(geom), dataset_id)`. This allows the same geometry
  to exist across different datasets while preventing duplicates within one.
- **Functional Indexes**: Implemented PostgreSQL functional indexes via Alembic
  to handle large geometry strings efficiently.
- **Natural Key Enforcement**: Added a unique index on `landiq_record.record_id`
  to support reliable upserts.

## Plan Status Assessment

Based on the `landiq_optimization_plan.md`, the current status of the
optimization effort is as follows:

| Step | Description                   | Status        | Notes                                          |
| ---- | ----------------------------- | ------------- | ---------------------------------------------- |
| 1    | Bulk Polygon "Insert-Ignore"  | **Completed** | Uses `md5(geom)` functional index.             |
| 2    | Multi-Table Bulk ID Retrieval | **Completed** | Implemented for Polygons, Crops, and Datasets. |
| 3    | In-Memory Normalization       | **Completed** | Handled via Pandas mapping in the load task.   |
| 4    | Bulk LandiqRecord Upsert      | **Completed** | Uses `ON CONFLICT (record_id) DO UPDATE`.      |
| 5    | macOS Compatibility           | **Completed** | `PROJ_LIB` environment fix implemented.        |

**Overall Plan Status: 100% Implemented.** The pipeline has been verified with a
full run of 446,713 features, confirming successful data population and
significantly improved performance.

## Installation & Setup

### Apply Schema Changes

To apply the new unique constraints and indexes:

```bash
pixi run migrate
```

### Running the Pipeline

The pipeline can be executed via the standard Prefect runner:

```bash
python resources/prefect/run_prefect_flow.py
```

## Technical Notes

- **Functional Indexing**: The use of `md5(geom)` in the unique constraint is
  critical for performance when dealing with complex WKT strings.
- **Reproducibility**: All manual database adjustments made during
  troubleshooting have been formalized into Alembic migrations
  ([`f7cda05a589d`](alembic/versions/f7cda05a589d_add_unique_constraints_to_landiqrecord_.py)
  and
  [`ffb2cf6b38b3`](alembic/versions/ffb2cf6b38b3_adding_dataset_id_to_polygon_unique_key.py)).
