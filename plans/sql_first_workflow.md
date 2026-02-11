# Plan: SQL-First Development Workflow with `pgschema`

This plan outlines the transition from a LinkML-first to a SQL-first development
workflow for schema modifications in the `ca-biositing` project. We will use
`pgschema` to provide a declarative "dump/edit/plan/apply" cycle, allowing for
rapid iteration during development.

## 🎯 Objectives

- Speed up schema modifications by working directly in SQL.
- Use `pgschema` for declarative schema management and migrations.
- Maintain LinkML as the long-term "steady state" source of truth.
- Update documentation and agent instructions to reflect this hybrid approach.

## 🏗️ Architecture

- **Desired State**: Represented by a multi-file SQL structure in
  `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/`.
- **Tooling**: `pgschema` for comparing local SQL files against the running
  PostgreSQL database.
- **Automation**: Pixi tasks for `schema-dump`, `schema-plan`, and
  `schema-apply`.
- **Dependency Management**: A custom utility `reorder_sql_main.py` ensures SQL
  files are included in the correct foreign-key order.

## 📝 Todo List

### 1. Environment & Dependencies

- [x] Add `pgschema` requirement documentation (system-level install).
- [x] Upgrade infrastructure to PostgreSQL 15.3 to support `pgschema` features.

### 2. Directory Initialization

- [x] Create the directory
      `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/`.
- [x] Capture current database state as the starting point using
      `pgschema dump`.

### 3. Pixi Task Implementation

- [x] Implement `schema-dump` task: Captures current DB state into the
      `sql_schemas/` directory.
- [x] Implement `schema-plan` task: Generates a migration plan using a shadow
      database (`biocirv_db_shadow`) for sandboxing.
- [x] Implement `schema-apply` task: Applies the generated changes to the local
      database.

### 4. Baselining & Ordering

- [x] Create `src/ca_biositing/datamodels/utils/reorder_sql_main.py` to automate
      topological sorting of SQL files.
- [x] Run the reordering utility to fix the `main.sql` include order.

### 5. Documentation & Agent Guidance

- [x] Create `docs/datamodels/SQL_FIRST_WORKFLOW.md` detailing the new workflow.
- [x] Update root `AGENTS.md` and `README.md` to explain the hybrid approach.
- [x] Update `src/ca_biositing/datamodels/AGENTS.md` and `README.md` with
      specific implementation details.

### 6. Verification & Testing

- [x] Perform a test schema change (Added `middle_name` to `contact` table).
- [x] Run `pixi run schema-plan` to verify the `ALTER` statement.
- [x] Document the entire implementation in a formal PR guide
      (`docs/pr/sql_first_workflow_implementation.md`).

## 🔄 Lifecycle: Development to Steady State

1. **Rapid Development**: Developers edit SQL files and use `pgschema` to update
   the DB.
2. **Review**: Changes are reviewed via `schema-plan` output.
3. **Steady State**: Once the schema is stable, LinkML YAMLs are updated to
   match the SQL source of truth.
4. **LinkML Sync**: `update-schema` is run once to ensure generated SQLAlchemy
   models and Alembic history remain consistent.
