# PR: Resolve Schema Desync, Editable Installs, and Functional Index Restoration

## Overview

This PR delivers a comprehensive fix for a series of interconnected issues that
were causing the Land IQ ETL pipeline to fail following a complete database
reset. The fixes address environment-level pathing discrepancies,
LinkML-to-SQLAlchemy generation limitations, and database schema alignment.

## Key Issues Resolved

### 1. The "Phantom Model" Problem & Editable Installs

**Issue**: Changes made to local source files in `src/ca_biositing/datamodels`
were not reflected at runtime. Python was importing stale SQLAlchemy models from
the `.pixi` environment's `site-packages` instead of the local `src/` directory.
This led to a critical discrepancy in how primary keys were handled between
SQLAlchemy and PostgreSQL. **Solution**:

- Updated [`pixi.toml`](pixi.toml) to use `editable = true` for all local
  namespace packages (`datamodels`, `pipeline`, `webservice`). This ensures that
  any changes to the source code or generated models are immediately visible to
  the Python interpreter.
- Modified [`alembic/env.py`](alembic/env.py) to prioritize local source code by
  adding `sys.path.insert(0, ...)` for the datamodels directory, ensuring
  Alembic always compares the database against the freshly generated models in
  `src/`.

### 2. LinkML Identifier & Composite PK Conflict

**Issue**: Marking `record_id` as `identifier: true` in LinkML caused the
generator to create a composite Primary Key `(id, record_id)`. This disabled
SQLAlchemy's `autoincrement` behavior for the `id` column, causing it to send
`NULL` values during inserts, which the database rejected. **Solution**:

- Removed `identifier: true` from
  [`landiq_record.yaml`](resources/linkml/modules/external_data/landiq_record.yaml).
- Updated [`generate_sqla.py`](resources/linkml/scripts/generate_sqla.py) to
  enforce `id` as the sole Primary Key with `autoincrement=True` and correctly
  handle `record_id` as a `UniqueConstraint`.

### 3. Missing Functional Unique Index on Polygon

**Issue**: Land IQ pipeline failed with
`(psycopg2.errors.InvalidColumnReference) there is no unique or exclusion constraint matching the ON CONFLICT specification`.
The high-performance "Insert-Ignore" logic for polygons requires a unique index
on `md5(geom)` and `dataset_id`. LinkML does not natively support PostgreSQL
functional indexes, so this index was lost during the database reset.
**Solution**:

- Modified [`generate_sqla.py`](resources/linkml/scripts/generate_sqla.py) to
  inject the functional index directly into the SQLAlchemy `Polygon` model's
  `__table_args__`.
- Added global injection of `text` and `Index` imports from `sqlalchemy` into
  the generated models to support these functional expressions.
- Refactored the post-processing logic to ensure these custom indexes coexist
  with Prefect's `extend_existing: True` requirement.

## Changes

### Environment & Configuration

- **[`pixi.toml`](pixi.toml)**: Switched local path dependencies to
  `editable = true`.
- **[`alembic/env.py`](alembic/env.py)**: Forced local path priority for model
  imports.

### Data Models & Generation

- **[`resources/linkml/modules/external_data/landiq_record.yaml`](resources/linkml/modules/external_data/landiq_record.yaml)**:
  Removed `identifier: true` from `record_id`.
- **[`resources/linkml/scripts/generate_sqla.py`](resources/linkml/scripts/generate_sqla.py)**:
  - Added global injection of `text` and `Index` imports.
  - Implemented specific injection for the `Polygon` table functional index.
  - Hardened regex patterns for Primary Key and Unique Constraint enforcement.

### Database Migrations

- **[`alembic/versions/c014594580cb_restore_functional_unique_index_to_.py`](alembic/versions/c014594580cb_restore_functional_unique_index_to_.py)**:
  New migration generated to restore the functional index on the `polygon`
  table.

## Verification Results

1.  **Schema Alignment**: Confirmed via `\d polygon` that the functional index
    `unique_geom_dataset_md5` is present.
2.  **Model Integrity**: Verified that `LandiqRecord` now uses a single `id`
    Primary Key with autoincrement.
3.  **Pipeline Success**: The Land IQ ETL pipeline now successfully bypasses the
    `ON CONFLICT` error and proceeds with bulk loading.
