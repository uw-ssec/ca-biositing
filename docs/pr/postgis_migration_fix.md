# PR: Fix PostGIS Table Drop in Alembic Migrations

## Description

Alembic's autogenerate feature was incorrectly detecting PostGIS internal tables
(like `spatial_ref_sys`) as tables to be dropped because they were present in
the database but not defined in the SQLAlchemy models. Attempting to run these
migrations resulted in a `psycopg2.errors.DependentObjectsStillExist` error
because PostGIS requires these tables.

## Steps to Reproduce

1. Have a database with the PostGIS extension enabled.
2. Run `pixi run update-schema` to generate a new migration.
3. Observe `op.drop_table('spatial_ref_sys')` in the generated migration file.
4. Run `pixi run migrate` and see it fail with:
   `psycopg2.errors.DependentObjectsStillExist: cannot drop table spatial_ref_sys because extension postgis requires it`

## Expected Behavior

Alembic should ignore internal PostGIS tables during the autogeneration process.

## Solution

Implemented an `include_object` filter in `alembic/env.py` to exclude the
following PostGIS-related tables from the migration generation:

- `spatial_ref_sys`
- `geometry_columns`
- `geography_columns`
- `raster_columns`
- `raster_overviews`

## Relevant Log Output

```shell
sqlalchemy.exc.InternalError: (psycopg2.errors.DependentObjectsStillExist) cannot drop table spatial_ref_sys because extension postgis requires it
HINT:  You can drop extension postgis instead.
[SQL: DROP TABLE spatial_ref_sys]
```

## Environment

- **Platform:** macOS (Sequoia)
- **Software Version:** Alembic >= 1.13.2, SQLAlchemy >= 2.0.0
- **Database:** PostgreSQL with PostGIS extension
