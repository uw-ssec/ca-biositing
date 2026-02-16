# Plan: Materialized Views Mapping & Analytics Layer

This plan outlines the implementation of an analytics layer using Materialized
Views in a dedicated `ca_biositing` database schema. The views are defined using
LinkML to ensure type safety and seamless integration with the existing data
models.

## 1. Architectural Strategy

### Dedicated Analytics Schema

All materialized views and analytical bridge tables will reside in a new
PostgreSQL schema: **`ca_biositing`**. The normalized source tables will remain
in the `public` schema.

### LinkML-First View Definitions

Materialized views will be defined as LinkML classes in a new module:
`resources/linkml/modules/ca_biositing_views/`.

- **Schema Mapping**: Use LinkML `annotations` or `notes` to store the
  underlying SQL query.
- **Table Arguments**: Use SQLAlchemy `__table_args__` via LinkML annotations to
  specify `schema: ca_biositing`.

## 2. Table Mapping & Gap Analysis

| ERD Table                  | Source Table(s)                                     | Status / Notes                                                   |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------- |
| `landiq_record_view`       | `landiq_record`, `polygon`, `primary_ag_product`    | **Initial View.** Combines crop data with geometry.              |
| `landiq_biomass_potential` | `landiq_record`, `polygon`, `resource_availability` | Calculates analytical potential per polygon.                     |
| `analysis_data_view`       | `observation`, `parameter`, `resource`, `unit`      | Denormalized analytical records.                                 |
| `landiq_resource_mapping`  | `landiq_resource_mapping`                           | **Implemented.** Bridge for crop-to-resource translation.        |
| `resource_availability`    | `resource_availability`                             | **Updated.** Regional residue factors for potential calculation. |

## 3. Initial View: `landiq_record_view`

This view serves as the baseline for spatial crop analysis, merging the record
metadata with the polygon geometry.

### LinkML Definition (Draft)

File: `resources/linkml/modules/ca_biositing_views/landiq_record_view.yaml`

```yaml
classes:
  LandiqRecordView:
    annotations:
      sql_schema: ca_biositing
      materialized: true
      sql_definition: >
        SELECT
          lr.record_id,
          p.geom,
          p.geoid,
          pap.name as crop_name,
          lr.acres,
          lr.irrigated,
          lr.confidence,
          lr.dataset_id
        FROM public.landiq_record lr JOIN public.polygon p ON lr.polygon_id =
        p.id JOIN public.primary_ag_product pap ON lr.main_crop = pap.id
    slots:
      - record_id
      - geom
      - geoid
      - crop_name
      - acres
      - irrigated
      - confidence
      - dataset_id
```

## 4. Advanced View: `landiq_biomass_potential_view`

Calculates theoretical biomass yield per polygon.

```sql
-- Resides in ca_biositing schema
CREATE MATERIALIZED VIEW ca_biositing.landiq_biomass_potential_view AS
SELECT
    lr.record_id,
    poly.geom,
    poly.geoid,
    pap.name AS crop_name,
    r.name AS internal_resource_name,
    lr.acres,
    ra.residue_factor_dry_tons_acre AS residue_factor,
    (lr.acres * COALESCE(ra.residue_factor_dry_tons_acre, 0)) AS estimated_dry_tons,
    lr.dataset_id
FROM public.landiq_record lr
JOIN public.polygon poly ON lr.polygon_id = poly.id
JOIN public.primary_ag_product pap ON lr.main_crop = pap.id
JOIN public.landiq_resource_mapping lrm ON lr.main_crop = lrm.landiq_crop_name
JOIN public.resource r ON lrm.resource_id = r.id
LEFT JOIN public.resource_availability ra ON
    ra.resource_id = r.id AND ra.geoid = poly.geoid;
```

## 5. Implementation Steps

### Phase 1: Schema & LinkML Setup

1.  **Create Directory**:
    `mkdir -p resources/linkml/modules/ca_biositing_views/`.
2.  **Define Views**: Create YAML files for each view in the new directory.
3.  **Update Root Schema**: Add the new module to
    `resources/linkml/ca_biositing.yaml` imports.

### Phase 2: Code Generation & Infrastructure

1.  **Modify Generator**: Update
    `src/ca_biositing/datamodels/utils/generate_sqla.py` to:
    - Detect `sql_schema` and `materialized` annotations.
    - Inject `__table_args__ = {"schema": "ca_biositing"}` into generated
      classes.
    - Handle views as `Table` objects with `Base.metadata` if they shouldn't be
      managed as standard tables by Alembic.
2.  **Schema Migration**: Create an Alembic migration that creates the
    `ca_biositing` schema:
    ```sql
    CREATE SCHEMA IF NOT EXISTS ca_biositing;
    ```

### Phase 3: View Creation & Orchestration

1.  **SQL Execution**: Create a utility to execute the `sql_definition` from
    LinkML to create/replace materialized views.
2.  **Prefect Task**: Add a task `refresh_materialized_views` to the end of
    relevant flows.

## 6. Implementation Notes (Updated)

1. **Observation Linking**: Observations link to context records (like
   `proximate_record`) via `record_id` and `record_type`. These context records
   contain the `resource_id`.
2. **Tileset Tracking**: A new explicit `tileset_id` column will be added to
   relevant records. This will be used to track Mapbox exports and trigger
   Prefect flows if data updates occur after the last "cut".
3. **LandIQ Mapping**: `landiq_resource_mapping` is **one-to-many** (one LandIQ
   `main_crop` can represent multiple internal `Resource` types).
4. **Residue Factors**: Factors are regional. If a specific `geoid` match is
   missing, the view currently returns 0 tons. A future enhancement should add a
   "Statewide Default" lookup.
