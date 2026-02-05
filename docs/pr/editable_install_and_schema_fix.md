# PR: Resolve Schema Desync via Editable Installs and LinkML Alignment

## Description

This PR addresses a persistent issue where the ETL pipelines (specifically the
LandIQ flow) were failing with `NotNullViolation` errors on the `id` column,
despite the database schema appearing correct.

The root cause was identified as a "Phantom Model" issue where the Python
environment was importing stale SQLAlchemy models from the `.pixi` environment's
`site-packages` instead of the local `src/` directory. This led to a critical
discrepancy in how primary keys were handled between SQLAlchemy and PostgreSQL.

## Key Findings

### 1. The "Phantom Model" Problem

Even when local source files in `src/ca_biositing/datamodels` were updated, the
changes were not reflected at runtime.

- **Symptom**: `psql` showed `id` as the sole Primary Key, but Python reported
  `record_id` as the Primary Key.
- **Cause**: Pixi was performing a "copy-style" install of local path
  dependencies. Python prioritized the copied files in `site-packages` over the
  local `src` directory.
- **Solution**: Updated [`pixi.toml`](pixi.toml) to use `editable = true` for
  all local namespace packages (`datamodels`, `pipeline`, `webservice`). This
  ensures that any changes to the source code or generated models are
  immediately visible to the Python interpreter.

### 2. LinkML Identifier Conflict

The `LandiqRecord` definition in LinkML was contributing to the creation of
composite primary keys.

- **Issue**: Marking `record_id` as `identifier: true` in LinkML caused the
  generator to mark it as a Primary Key. Since the class also inherited `id`
  from `BaseEntity`, SQLAlchemy created a composite PK `(id, record_id)`.
- **Impact**: Composite primary keys disable SQLAlchemy's default
  `autoincrement` behavior for the `id` column, causing it to send `NULL` values
  during inserts, which the database rejected.
- **Fix**: Removed `identifier: true` from
  [`landiq_record.yaml`](resources/linkml/modules/external_data/landiq_record.yaml)
  and relied on `unique_keys` for business identifiers.

### 3. Chain of Truth Alignment

We verified the alignment across the entire stack:

1. **LinkML**: Now defines `record_id` as a regular slot with a unique
   constraint.
2. **SQLAlchemy (Local)**: Now correctly identifies `id` as the sole
   `primary_key=True` with `autoincrement=True`.
3. **Database**: Confirmed via `\d landiq_record` to have the correct PK and
   sequence defaults.

## Changes

- **[`pixi.toml`](pixi.toml)**: Added `editable = true` to local
  pypi-dependencies.
- **[`resources/linkml/modules/external_data/landiq_record.yaml`](resources/linkml/modules/external_data/landiq_record.yaml)**:
  Removed `identifier: true` from `record_id`.
- **[`src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/ca_biositing.py`](src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/ca_biositing.py)**:
  Regenerated models now correctly reflect the single primary key.

## Verification Results

- **Import Path**: Confirmed `ca_biositing.datamodels` now loads from the local
  `src` directory.
- **Model Inspection**: Confirmed `LandiqRecord.__table__.primary_key` only
  contains the `id` column.
- **ETL Progress**: The LandIQ flow now successfully bypasses the
  `NotNullViolation` and proceeds to the data loading phase.

## Next Steps

- Resolve the `ON CONFLICT` specification mismatch in the `Polygon` table upsert
  logic.
