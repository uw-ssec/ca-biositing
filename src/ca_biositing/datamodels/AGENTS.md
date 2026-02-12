# AGENTS.md - CA Biositing Data Models

This file provides guidance to AI assistants when working with the
`ca-biositing-datamodels` namespace package.

## Package Overview

This is the **ca-biositing-datamodels** package, a PEP 420 namespace package
containing SQLAlchemy database models for the CA Biositing project. It is
designed to be shared across multiple components (ETL pipelines, API services,
analysis tools) of the parent ca-biositing project.

**Package Stats:**

- **Type:** Python namespace package (PEP 420)
- **Package Name:** `ca-biositing-datamodels`
- **Import Name:** `ca_biositing.datamodels`
- **Version:** 0.1.0
- **Python:** >= 3.12
- **Build System:** Hatchling
- **License:** BSD License
- **Domain:** Database models, SQLAlchemy, PostgreSQL, LinkML

## Cross-Cutting Documentation

This package follows project-wide patterns documented in:

| Topic              | Document                                                           | When to Reference                          |
| ------------------ | ------------------------------------------------------------------ | ------------------------------------------ |
| Namespace Packages | [namespace_packages.md](../../../agent_docs/namespace_packages.md) | Import errors, package structure questions |
| Testing Patterns   | [testing_patterns.md](../../../agent_docs/testing_patterns.md)     | Writing tests, fixtures, pytest commands   |
| Code Quality       | [code_quality.md](../../../agent_docs/code_quality.md)             | Pre-commit, style, imports                 |
| Troubleshooting    | [troubleshooting.md](../../../agent_docs/troubleshooting.md)       | Common errors and solutions                |

```text
src/ca_biositing/datamodels/
├── ca_biositing/              # No __init__.py at this level (namespace)
│   └── datamodels/            # Package implementation
│       ├── __init__.py        # Package initialization
│       ├── database.py        # Connection and session management
│       ├── linkml/            # LinkML source of truth (YAML)
│       ├── schemas/
│       │   └── generated/     # Generated SQLAlchemy classes (DO NOT EDIT)
│       └── utils/             # Orchestration and generation scripts
├── tests/                     # Test suite
├── pyproject.toml            # Package metadata
└── README.md                 # Documentation
```

**CRITICAL:** The `ca_biositing/` directory does **NOT** have an `__init__.py`
file. This allows multiple packages to share the `ca_biositing` namespace.

### Model Architecture (Hybrid Workflow)

This project uses a hybrid schema management approach:

1.  **SQL-First (Development)**: Rapidly iterate by modifying SQL files in
    `sql_schemas/` and using `pgschema`.
2.  **LinkML (Steady State)**: Once stable, changes are synced back to LinkML
    YAML definitions for long-term tracking and model generation.

- **SQL Source**:
  `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/`
- **LinkML Source**:
  `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/`
- **Generated Models**:
  `src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/`

**DO NOT EDIT the generated Python files directly.**

### Note on Unique Constraints

LinkML's SQLAlchemy generator does not always preserve `UNIQUE` constraints or
`identifier` status in a way that Alembic detects for all polymorphic tables.
The `generate_sqla.py` script includes a post-processing step to manually inject
`unique=True` for `record_id` on target classes (Observations and Aim Records)
to ensure robust upsert support.

## Schema Management Workflow (CRITICAL)

### Development Shortcut (SQL-First)

For rapid iteration, work directly in SQL:

1.  **Modify SQL**: Edit `.sql` files in
    `src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas/`.
2.  **Plan**: `pixi run schema-plan`.
3.  **Apply**: `pixi run schema-apply`.

See
[docs/datamodels/SQL_FIRST_WORKFLOW.md](../../../docs/datamodels/SQL_FIRST_WORKFLOW.md)
for details.

### Steady State Sync (LinkML)

Once the schema stabilizes, sync back to the main data model.

### 1. Update LinkML

Modify the YAML files in the `linkml/modules/` directory to match the SQL state.

### 2. Orchestrate Update

Run the following command from the project root:

```bash
pixi run update-schema -m "Description of changes"
```

This task executes
[`orchestrate_schema_update.py`](src/ca_biositing/datamodels/utils/orchestrate_schema_update.py)
which:

- Generates SQLAlchemy models from LinkML.
- Rebuilds Docker services.
- **Generates the Alembic migration LOCALLY** to avoid container import hangs.

### 3. Apply Migrations

Apply changes to the database:

```bash
pixi run migrate
```

_Note: This runs `alembic upgrade head` locally against the Docker-hosted
PostgreSQL._

## Dependencies & Environment

### Core Dependencies

From `pyproject.toml`:

- **SQLAlchemy** (>=2.0.0): SQL database ORM
- **Alembic** (>=1.13.2, <2): Database migrations
- **psycopg2-binary** (>=2.9.6, <3): PostgreSQL adapter
- **LinkML** (>=1.8.0): Data modeling framework
- **Pydantic** (>=2.0.0): Data validation
- **Pydantic Settings** (>=2.0.0): Configuration management

### Development Environment

This package is typically developed as part of the main ca-biositing project
using Pixi.

**For testing this package:**

```bash
# From the main project root
pixi run pytest src/ca_biositing/datamodels -v
```

## Code Quality & Standards

### Pre-commit Checks

Always run pre-commit before committing:

```bash
# From main project root
pixi run pre-commit run --files src/ca_biositing/datamodels/**/*
```

### Import Conventions

```python
# Standard library
from __future__ import annotations
from datetime import datetime
from typing import Optional

# Third-party
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Local (Generated models)
from ca_biositing.datamodels.schemas.generated.ca_biositing import Resource
```

## Common Pitfalls & Solutions

### Issue: Import errors with namespace package

**Solution:** Ensure `ca_biositing/` does **NOT** have `__init__.py`. Ensure you
are running inside the Pixi environment (`pixi run ...`) where all namespace
packages are installed. See root `AGENTS.md` for details.

### Issue: Alembic hangs in Docker

**Solution:** Always use `pixi run update-schema` and `pixi run migrate`. These
are configured to run locally to bypass Docker Desktop performance issues on
macOS.

## Related Documentation

- **Main Project AGENTS.md**: `AGENTS.md` (root)
- **Package README**: `src/ca_biositing/datamodels/README.md`
- **Notebook Setup**: `docs/notebook_setup.md`
