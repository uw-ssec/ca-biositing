# Plan: Multi-Schema Implementation (ca_biositing & beam_portal)

This plan outlines the implementation of two dedicated PostgreSQL schemas to
support different downstream applications, managed via LinkML and Alembic.

## 1. Schema Architecture

- **`public`**: Internal normalized data layer (ETL target).
- **`ca_biositing`**: Geospatial tool layer. Contains views optimized for QGIS
  and geospatial analysis.
- **`beam_portal`**: Analytics layer (replaces `analytics`). Contains
  denormalized fact tables for CubeJS.

## 2. Implementation Steps

### Phase 1: LinkML Schema Definition

- [ ] Create LinkML modules:
  - `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/ca_biositing/`
  - `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/beam_portal/`
- [ ] Define classes/views in each module with `sql_view` annotations.
- [ ] Update main `ca_biositing.yaml` to import these modules.

### Phase 2: SQLAlchemy Model Generation

- [ ] Update `src/ca_biositing/datamodels/utils/generate_sqla.py` to:
  - Detect module path for each class.
  - Map `ca_biositing` module to `ca_biositing` schema.
  - Map `beam_portal` module to `beam_portal` schema.
  - Inject `__table_args__ = {'schema': '...'}` accordingly.

### Phase 3: Reproducible Database Setup (Alembic)

- [ ] Update `alembic/env.py` to support multiple schemas
      (`include_schemas=True`).
- [ ] Create a manual Alembic migration to:
  - `CREATE SCHEMA IF NOT EXISTS ca_biositing;`
  - `CREATE SCHEMA IF NOT EXISTS beam_portal;`
  - Create views in respective schemas.
  - Setup roles: `beam_reader` (for CubeJS) and `gis_reader` (for geospatial
    tools).
  - Grant permissions specifically to the relevant schemas.

### Phase 4: Validation

- [ ] Run `pixi run update-schema` and verify generated Python models.
- [ ] Run `pixi run migrate` and verify schema/view existence in Postgres.
- [ ] Verify partner access isolation (e.g., `beam_reader` cannot see
      `ca_biositing` views).

## 3. Security Model (Alembic Snippet)

```sql
-- beam_portal permissions
GRANT USAGE ON SCHEMA beam_portal TO beam_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA beam_portal TO beam_reader;

-- ca_biositing permissions
GRANT USAGE ON SCHEMA ca_biositing TO gis_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA ca_biositing TO gis_reader;
```
