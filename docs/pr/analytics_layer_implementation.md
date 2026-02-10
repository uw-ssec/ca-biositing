# PR Summary: Implementation of Analytics Layer and Materialized Views

## Overview

This PR implements the initial version of the **Analytics Layer** for the
`ca-biositing` project. The core architectural goal is to provide a
denormalized, high-performance interface for geospatial analysis and frontend
access while maintaining LinkML as the single source of truth for the entire
data model.

## Key Components

### 1. Dedicated `ca_biositing` Schema

We have introduced a new PostgreSQL schema: **`ca_biositing`**.

- **Purpose**: This schema is reserved exclusively for analytical views,
  tileset-optimized tables, and denormalized records.
- **Isolation**: By keeping analytical logic in a separate schema from the
  `public` schema (where normalized source data resides), we ensure that ETL
  processes and analytics remains decoupled and manageable.
- **Migration**: A dedicated Alembic migration
  ([`alembic/versions/90df744a03b4_create_ca_biositing_schema.py`](alembic/versions/90df744a03b4_create_ca_biositing_schema.py))
  was created to initialize this schema.

### 2. LinkML-First View Definitions

Following project standards, all analytical views are defined as LinkML classes
in a new module: `resources/linkml/modules/ca_biositing_views/`.

- **Metadata Integration**: Each `.yaml` file uses LinkML `annotations` to store
  its underlying SQL query (`sql_definition`) and target schema (`sql_schema`).
- **Type Safety**: Defining views in LinkML allows us to generate Python models
  that provide IDE autocompletion and type checking for the denormalized data.
- **Implemented Modules**:
  - `landiq_record_view.yaml`: baseline spatial crop analysis.
  - `analysis_data_view.yaml`: Denormalized biomass observations joined with
    resource metadata.
  - `landiq_tileset_view.yaml`: Geometry-heavy view optimized for Mapbox tileset
    exports.
  - `usda_census_view.yaml` & `usda_survey_view.yaml`: Denormalized USDA
    agricultural statistics.

### 3. Automated Model Generation

The SQLAlchemy generator
([`src/ca_biositing/datamodels/utils/generate_sqla.py`](src/ca_biositing/datamodels/utils/generate_sqla.py))
has been enhanced to:

- Parse the analytical LinkML modules.
- Automatically inject `__table_args__` into the generated Python classes.
- Store the SQL definition in the SQLAlchemy `info` dictionary, paving the way
  for future Alembic automation.

### 4. Standalone View Orchestration

To enable rapid testing and deployment, we have established a standalone
orchestration script:
[`resources/sql/create_analytical_views.sql`](resources/sql/create_analytical_views.sql).

- **Workflow**:
  1. Define the logic in LinkML.
  2. Sync the logic to the `.sql` script.
  3. Execute the script to refresh materialized views.
- **Indices**: The script automatically creates GIST spatial indices on relevant
  views to ensure high-performance geospatial queries.

## Issues and Refinements

- **Join Logic**: Refined `analysis_data_view` to correctly navigate the
  hierarchy from Observations through Prepared Samples and Field Samples to
  reach the Resource name.
- **Data Types**: Implemented explicit casting (e.g., `record_id::text`) to
  resolve type mismatches between generic observation fields and source primary
  keys.
- **Schema Detection**: Documented current challenges with Alembic's automatic
  detection of view-specific metadata in
  [`docs/pr/alembic_materialized_view_automation.md`](docs/pr/alembic_materialized_view_automation.md).

## Verification Results

- **Schema successfully created.**
- **5 Materialized Views successfully deployed.**
- **Verified Data Population**:
  - `analysis_data_view`: 1,750 records populated with resource names.
  - `landiq_tileset_view`: 156,638 records with spatial indices.
