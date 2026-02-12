> **Historical Document**: This PR description is preserved for reference. The
> LinkML code generation workflow described below has been replaced by
> hand-written SQLModel classes with Alembic migrations. See the
> [datamodels README](../../src/ca_biositing/datamodels/README.md) for the
> current workflow.

# LinkML and SQLAlchemy Integration (Archived)

This PR introduces a robust, schema-first approach to data modeling using
**LinkML** as the source of truth. This architecture ensures that our database
schema, Python models, and documentation remain perfectly synchronized.

## Core Architecture

### LinkML Source of Truth

The data model is defined using LinkML YAML modules located in:
`src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/`

These modules cover core entities, geospatial polygons, ETL lineage, and
domain-specific records (Aim 1, Aim 2, LandIQ, USDA).

### Automated SQLAlchemy Generation

We use a custom orchestration script, `generate_sqla.py`, to transform LinkML
YAML definitions into SQLAlchemy ORM classes.

**Key Features of `generate_sqla.py`:**

- **Automated Mapping**: Converts LinkML classes, slots, and types into
  SQLAlchemy tables and columns.
- **Post-Processing for Upserts**: LinkML's default generator sometimes misses
  critical database constraints. Our script manually injects `unique=True` for
  `record_id` fields on Observations and Aim Records. This is essential for our
  "upsert" (update or insert) logic in the ETL pipeline.
- **Polymorphic Support**: Correctly handles inheritance patterns defined in
  LinkML for complex record types.

## Schema Management Workflow

To maintain the integrity of the database while avoiding performance issues
(especially on macOS Docker environments), we have implemented a specialized
workflow:

1.  **Modify Schema**: Edit YAML files in `linkml/modules/`.
2.  **Orchestrate Update**: Run `pixi run update-schema`. This executes
    `orchestrate_schema_update.py`, which:
    - Generates the Python SQLAlchemy models.
    - Rebuilds the relevant Docker services.
    - **Generates the Alembic migration LOCALLY**. This is a critical
      optimization that prevents the common "Alembic hang" seen when trying to
      import heavy models inside a container.
3.  **Apply Migrations**: Run `pixi run migrate` to apply the changes to the
    PostgreSQL database.

## Benefits to Upstream

- **Type Safety**: Pydantic and SQLAlchemy models are strictly typed based on
  the schema.
- **Maintainability**: Adding a new field only requires a single change in a
  YAML file.
- **Consistency**: The same schema can be used to generate JSON-LD, SHACL, or
  Markdown documentation in the future.
- **Performance**: Local migration generation significantly speeds up the
  development cycle.

## Relevant Files

- `src/ca_biositing/datamodels/utils/generate_sqla.py`: The core generation
  logic.
- `src/ca_biositing/datamodels/utils/orchestrate_schema_update.py`: The task
  runner for schema updates.
- `src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/`: The
  output directory for generated models (DO NOT EDIT).
