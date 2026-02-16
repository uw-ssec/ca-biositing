# Alembic Materialized View Automation: Summary & Issues

## Overview

This document summarizes the effort to automate the creation of PostgreSQL
Materialized Views within the `ca_biositing` analytics schema using LinkML
definitions and Alembic migrations.

## Changes Implemented

### 1. LinkML Definition

- Created `resources/linkml/modules/ca_biositing_views/landiq_record_view.yaml`.
- Used LinkML `annotations` to store:
  - `sql_schema: ca_biositing`
  - `materialized: true`
  - `sql_definition: SELECT ...`

### 2. SQLAlchemy Generator (`src/ca_biositing/datamodels/utils/generate_sqla.py`)

- Updated the generator to parse LinkML YAML files in the `ca_biositing_views`
  module.
- Modified the post-processor to inject `__table_args__` into the generated
  SQLAlchemy classes.
- The injection includes:
  - `schema: 'ca_biositing'`
  - `info: {'is_materialized_view': True, 'sql_definition': r'''...'''}`

### 3. Alembic Configuration (`alembic/env.py`)

- Integrated `alembic.autogenerate.rewriter.Rewriter`.
- Added a rewrite rule for `ops.CreateTableOp`:
  - Detects if `is_materialized_view` is present in the table's `info`
    dictionary.
  - If found, it replaces the standard `CREATE TABLE` operation with a
    `ops.ExecuteSQLOp` that runs `CREATE MATERIALIZED VIEW ... AS ...`.
- Added a rewrite rule for `ops.DropTableOp` to handle `DROP MATERIALIZED VIEW`
  for the `ca_biositing` schema.

## Issues Encountered

### 1. Metadata Propagation

The primary issue is that **SQLAlchemy's `Table.info` dictionary is not
automatically passed to Alembic's `CreateTableOp` during the autogenerate
phase.**

When Alembic compares the metadata to the database:

1. It sees a new class in the Python code (`LandiqRecordView`).
2. It generates a standard `CreateTableOp`.
3. Even though the Python class has the `info` dict, the `CreateTableOp` object
   created by Alembic's internal "comparator" logic does not contain that `info`
   payload.
4. Consequently, our `Rewriter` hook in `env.py` sees `op.info` as `None` or
   empty, failing to trigger the custom SQL injection.

### 2. Standard Table Generation

Because the detector fails, Alembic continues to generate a standard
`op.create_table(...)` command in the migration file, which is incorrect for a
materialized view.

## Potential Next Steps

1.  **Custom Alembic Comparator**: Implement a custom comparator using
    `@autogenerate.comparators.dispatch.register` to manually extract the `info`
    dict from the SQLAlchemy `Table` object and attach it to the Alembic
    `Operation` object.
2.  **Naming Convention**: Use a naming convention (e.g., classes ending in
    `...View`) to trigger the rewrite, though this is less robust than using
    metadata.
3.  **Manual SQL (Backburner)**: As an interim solution, use a standalone SQL
    script (`resources/sql/create_analytical_views.sql`) to create and manage
    views until the Alembic pipeline is fully stabilized.
4.  **Alembic-Utils/SQLAlchemy-Views**: Explore third-party libraries like
    `alembic-utils` or `sqlalchemy-views` which provide first-class support for
    view autogeneration.
