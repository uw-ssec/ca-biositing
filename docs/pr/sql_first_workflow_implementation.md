# PR: SQL-First Schema Development Path with `pgschema`

## Overview

This PR implements a new, streamlined development path for database schema
modifications. By introducing a SQL-first workflow powered by `pgschema`,
developers can bypass the complex LinkML -> SQLAlchemy -> Alembic pipeline
during rapid iteration phases.

## Changes

### 1. Tooling: `pgschema` Integration

- Integrated `pgschema`, a declarative schema management tool that provides a
  "dump/edit/plan/apply" workflow similar to Terraform.
- Added Pixi tasks to automate the cycle:
  - `pixi run schema-dump`: Captures the current database state into organized
    SQL files.
  - `pixi run schema-plan`: Generates a migration plan comparing local SQL files
    to the live database.
  - `pixi run schema-apply`: Safely applies schema changes to the database.
- Created a utility script
  [`src/ca_biositing/datamodels/utils/reorder_sql_main.py`](src/ca_biositing/datamodels/utils/reorder_sql_main.py)
  to automatically calculate the correct creation order for tables based on
  foreign key dependencies.

### 2. Infrastructure: PostgreSQL Upgrade

- **Upgraded PostgreSQL from 13.5 to 15.3** in
  `resources/docker/docker-compose.yml`.
- **Reasoning**: `pgschema` requires PostgreSQL 14+ to utilize modern catalog
  functions (specifically `pg_get_function_sqlbody`) for accurate declarative
  planning.
- **Impact**: Merging this change requires all developers to run
  `pixi run teardown-services-volumes` to wipe their local PostgreSQL 13 data
  volumes, as major version upgrades are not backward compatible at the storage
  layer.

### 3. Data Models: SQL Schema Tracking

- Created a new directory structure for tracking the "Desired State" of the
  database in raw SQL:
  - `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/`
- Organized the schema into multi-file outputs to improve Git visibility and
  maintainability.

### 4. Documentation

- Created
  [`docs/datamodels/SQL_FIRST_WORKFLOW.md`](docs/datamodels/SQL_FIRST_WORKFLOW.md)
  to guide the team through the new process.
- Updated root and package-level `AGENTS.md` and `README.md` files to reflect
  the hybrid approach.

### 5. Analytics Layer & Multi-Schema Integration

- **Consolidated Analytics**: Migrated the standalone analytics layer into the
  `pgschema` workflow. Materialized views are now tracked as individual SQL
  files in
  `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/ca_biositing/views/`.
- **Multi-Schema Orchestration**: Restructured the tracking to support both
  `public` and `ca_biositing` schemas. The `main.sql` file now acts as a global
  manifest, ensuring correct topological ordering across schemas.
- **Enhanced Task Suite**: Added specific Pixi tasks (`schema-analytics-plan`,
  `schema-analytics-apply`, `schema-analytics-refresh`) to manage the analytics
  lifecycle independently from core table modifications.
- **Conflict Resolution**: Removed redundant table definitions in the `public`
  schema to ensure the `ca_biositing` materialized views serve as the
  authoritative analytics layer.

## Troubleshooting & Installation

- `pgschema` is a Go-based binary. macOS users should install it via Homebrew:
  ```bash
  brew tap pgplex/pgschema
  brew install pgschema
  ```
- If planning fails with "relation does not exist" errors, run the reordering
  utility:
  ```bash
  python src/ca_biositing/datamodels/utils/reorder_sql_main.py
  ```

## Status: Completed

- [x] Initialize directory structure
- [x] Configure Pixi tasks
- [x] Upgrade PostgreSQL infrastructure
- [x] Capture baseline schema and fix dependency ordering
- [x] Finalize documentation
- [x] Verify workflow with test modification (Added `middle_name` to `contact`
      table)
- [x] Integrate analytics layer (materialized views) into multi-schema workflow
