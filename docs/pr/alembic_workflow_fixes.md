# PR: Resolve Schema Desync and Primary Key Constraints

## Description

This PR addresses a critical issue where Alembic migrations were failing to
detect new schema changes (such as the addition of the `county` column in
`LandiqRecord`) and were incorrectly generating composite primary keys that
disabled database autoincrement.

## Key Changes

### 1. Forced Local Model Imports in Alembic

The primary fix involves modifying [`alembic/env.py`](alembic/env.py) to
prioritize local source code over installed packages.

- **Issue**: Alembic was importing models from the `.pixi` environment's
  `site-packages`. If the environment wasn't refreshed after a LinkML change,
  Alembic would compare the database against an outdated "phantom" version of
  the models.
- **Fix**: Added
  `sys.path.insert(0, str(PROJECT_ROOT / "src/ca_biositing/datamodels"))` to the
  top of `env.py`. This ensures that the freshly generated models in `src/` are
  always used for migration generation.

### 2. Refactored Primary Key Logic in `generate_sqla.py`

Updated the post-processing script to ensure stable database constraints.

- **Single Primary Key**: Refactored the regex logic to ensure that `id` (from
  `BaseEntity`) is the **sole** primary key. Previously, `record_id` was also
  being marked as a primary key, creating a "Composite Primary Key" which caused
  SQLAlchemy to disable autoincrement and attempt to insert `NULL` values.
- **Unique Constraints**: `record_id` is now correctly handled as a
  `UniqueConstraint` rather than a primary key, maintaining data integrity for
  ETL upserts while allowing PostgreSQL to handle ID generation.
- **Robust Fallback**: Improved the fallback logic for models without an `id`
  column (e.g., `Place`, `Infrastructure`) to correctly identify identifiers.

## Verification Results

- **Migration Accuracy**: Confirmed that `alembic revision --autogenerate` now
  correctly detects all columns (including `county`) and generates the expected
  `PrimaryKeyConstraint('id')`.
- **ETL Success**: Verified that the `analysis_records.py` flow now completes
  successfully without `IntegrityError` or constraint violations.
- **Clean Slate**: Successfully performed a full database reset and verified
  that the initial migration perfectly matches the LinkML source of truth.
