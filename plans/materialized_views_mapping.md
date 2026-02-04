# Plan: Materialized Views Mapping & Schema Gap Analysis

This plan outlines the mapping between the proposed analytics layer (from
LucidChart ERD) and the existing normalized database schema, identifying gaps
and drafting the necessary queries.

## 1. Table Mapping & Gap Analysis

| ERD Table                        | Existing Normalized Table(s)                          | Gaps / Notes                                                     |
| -------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------- |
| `analysis_data`                  | `observation`, `parameter`, `unit`, `resource`        | Needs join across these tables.                                  |
| `landiq_tileset`                 | `landiq_record`, `polygon`, `place`                   | `tileset_id` is missing in `landiq_record`.                      |
| `landiq_resource_mapping`        | **MISSING**                                           | New bridge table needed to map `PrimaryAgProduct` to `Resource`. |
| `usda_survey`                    | `usda_survey_record`, `usda_commodity`, `observation` | Needs join to `observation` for values.                          |
| `billion_ton_tileset`            | `billion_ton2023_record`, `resource`                  | `tileset_id` is missing.                                         |
| `generic_infrastructure_tileset` | `facility_record`, `location_address`                 | `tileset_id` and `descriptor` mapping needed.                    |
| `location_address`               | `location_address`                                    | Existing.                                                        |
| `tileset_tracking`               | **MISSING**                                           | New metadata table for tileset management.                       |
| `usda_census`                    | `usda_census_record`, `usda_commodity`, `observation` | Needs join to `observation`.                                     |
| `landiq_usda_mapping`            | `resource_usda_commodity_map`                         | Existing mapping table can serve this purpose.                   |
| `resource_availability`          | `resource_availability`                               | Existing, but ERD implies specific foreign keys.                 |

## 2. Proposed Bridge Tables (LinkML)

### `landiq_resource_mapping`

Maps `PrimaryAgProduct` (used in LandIQ) to the internal `Resource` definition.

- `main_crop_id` (FK to `primary_ag_product`)
- `resource_id` (FK to `resource`)
- `collected` (boolean)

### `tileset_tracking`

Metadata for generated vector/raster tilesets.

- `name` (string)
- `tileset_type` (string: geom/point)
- `dataset_id` (FK to `dataset`)
- `data_size_mb` (float)

## 3. View Query Drafts

### View: `analysis_data_view`

```sql
-- Observations link to resources via their polymorphic record_id and record_type.
-- The associated record (e.g., proximate_record, ultimate_record) contains the resource_id.
SELECT
    o.id,
    r.name as resource,
    o.geoid,
    p.name as parameter,
    o.value,
    u.name as unit
FROM observation o
JOIN parameter p ON o.parameter_id = p.id
JOIN unit u ON o.unit_id = u.id
-- Example join for proximate records; in practice, this may need to be a UNION or dynamic join
LEFT JOIN proximate_record pr ON o.record_id = pr.record_id AND o.record_type = 'proximate_record'
LEFT JOIN resource r ON pr.resource_id = r.id;
```

### View: `landiq_tileset_view`

```sql
SELECT
    lr.id,
    poly.geom,
    pap.name as main_crop,
    lr.acres,
    lr.county,
    poly.geoid,
    lr.dataset_id as tileset_id -- Assuming dataset_id maps to tileset_id
FROM landiq_record lr
JOIN polygon poly ON lr.polygon_id = poly.id
JOIN primary_ag_product pap ON lr.main_crop = pap.id;
```

## 4. Implementation Steps

1.  **Update LinkML Schema**:
    - Add `landiq_resource_mapping` to
      `src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/external_data/`.
    - Add `tileset_tracking` to a new metadata module.
2.  **Generate Models & Migrations**:
    - Run `pixi run update-schema`.
    - Run `pixi run migrate`.
3.  **Create Materialized Views**:
    - Implement views in the `ca_biositing` or `beam_portal` schema as per
      `plans/analytics_schema_implementation.md`.

## 5. Implementation Notes (Updated)

1. **Observation Linking**: Observations link to context records (like
   `proximate_record`) via `record_id` and `record_type`. These context records
   contain the `resource_id`.
2. **Tileset Tracking**: A new explicit `tileset_id` column will be added to
   relevant records. This will be used to track Mapbox exports and trigger
   Prefect flows if data updates occur after the last "cut".
3. **LandIQ Mapping**: `landiq_resource_mapping` is **one-to-many** (one LandIQ
   `main_crop` can represent multiple internal `Resource` types).
