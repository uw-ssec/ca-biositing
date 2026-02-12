# SQL-First Schema Development Workflow

This document outlines the **SQL-first** development path for database schema
modifications in the CA Biositing project. This workflow allows for rapid
iteration by working directly in SQL, while maintaining LinkML as the long-term
source of truth for "steady state" synchronization.

## 🚀 Overview

The project uses `pgschema`, a declarative schema management tool, to
synchronize your local SQL "Desired State" with the PostgreSQL database. This
bypasses the LinkML -> SQLAlchemy -> Alembic pipeline during the active
development phase.

## 🛠 Prerequisites

### 1. Install `pgschema`

`pgschema` is a Go-based binary and must be installed manually on your system:

```bash
# macOS (Homebrew)
brew tap pgplex/pgschema
brew install pgschema
```

### 2. Infrastructure Upgrade

The project has been upgraded to **PostgreSQL 15**. If you are upgrading from an
older version, you must wipe your local data volumes:

```bash
pixi run teardown-services-volumes
pixi run start-services
```

## 🔄 The Development Cycle

### 1. Edit SQL Files

Schema definitions are organized by schema:

- **Public Schema** (Core Tables):
  `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/tables/`
- **Analytics Schema** (Materialized Views):
  `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/ca_biositing/views/`

Modify the `.sql` files to reflect your desired state.

### 2. Plan Changes

Choose the appropriate command based on which schema you are modifying:

#### For Core Tables (public schema):

```bash
pixi run schema-plan
```

#### For Analytical Views (ca_biositing schema):

```bash
pixi run schema-analytics-plan
```

Review the output to ensure it matches your intentions and doesn't contain
destructive changes you didn't expect.

### 3. Apply Changes

#### For Core Tables:

```bash
pixi run schema-apply
```

#### For Analytical Views:

```bash
pixi run schema-analytics-apply
```

### 4. Refreshing Data

Materialized views do not update automatically. After loading new data into the
public tables, refresh the analytical layer:

```bash
pixi run schema-analytics-refresh
```

To see the status of your views:

```bash
pixi run schema-analytics-list
```

### 4. Baseline (Optional)

If you've made manual changes to the database and want to bring them into your
SQL files:

```bash
pixi run schema-dump
```

_Note: This will overwrite your local SQL files with the current state of the
database._

## 🏁 Reaching Steady State

Once your schema changes have reached a stable point and you are ready to "sync
back" to the primary data model:

1.  **Update LinkML**: Manually update the LinkML YAML files in
    `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/` to
    match your new SQL schema.
2.  **Generate Models**: Run the standard orchestration task to update the
    SQLAlchemy models and create a formal Alembic migration for production
    tracking:
    ```bash
    pixi run update-schema -m "Syncing SQL-first development changes"
    ```

## ⚠️ Important Rules

1.  **Do Not Edit `generated/` files**: SQLAlchemy models in the `generated/`
    folder are still managed by LinkML. They will only reflect your SQL changes
    _after_ you perform a Steady State sync.
2.  **Git Tracking**: Always commit your changes to `sql_schemas/` as they
    represent the source of truth during development.
3.  **Data Loss**: Be aware that `pgschema apply` may perform destructive
    operations (like dropping columns) if they are removed from your SQL files.
    Always check `schema-plan` first.
