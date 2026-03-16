# Handoff: Materialized Views Revision

**Context:** The core join logic for the `data_portal` materialized views has
been updated to align with the BIOCIRV Specification. Migrations have been
applied and views are populated.

**Current Status:**

- `Resource` table has a new `uri` column.
- `mv_biomass_search` is fully implemented with aggregated moisture, sugar
  (glucose+xylose), and analytical flags.
- Experimental metadata (Method names) are joined into
  fermentation/gasification.
- Unique indexes exist for all views to support `REFRESH CONCURRENTLY`.

**Immediate Next Steps for the Agent:**

1. **Debug Fermentation View:** `mv_biomass_fermentation` currently returns 0
   rows. Investigate if the `Observation` table uses
   `record_type='fermentation'` or something else.
2. **Pretreatment Integration:** Incorporate specific measurement columns from
   `pretreatment_record` into the views.
3. **Phase 2 Tags:** Implement the logic to derive descriptive tags (e.g., "high
   moisture") based on whether a resource is in the top/bottom 10% for its
   category.
4. **Pricing View:** Finalize `mv_biomass_pricing` once the source columns in
   `UsdaMarketRecord` are ready.

---

# Plan: BIOCIRV Materialized Views Revision

This plan outlines the revisions required for the `data_portal` materialized
views to align with the [BIOCIRV-Materialized Views
Specification-160326-153133.pdf](plans/BIOCIRV-Materialized Views
Specification-160326-153133.pdf).

## 1. Overview of Gaps

The current implementation in
[`data_portal_views.py`](src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views.py)
lacks several pre-aggregated metrics and experimental metadata fields required
by the frontend prototype.

## 2. Revision Details

### 2.1 `mv_biomass_search`

- **Grain:** One row per `Resource`.
- **Literature URI:** Map from a new `uri` column on the `Resource` table (to be
  added).
- **Sugar Content:** Individual column for `sugar_content_percent`. Calculated
  as sum of averages for parameters "glucose" and "xylose".
- **Compositional Averages:** Individual columns for `moisture_percent`,
  `ash_percent`, and `lignin_percent`. Calculated as `avg(value)` for
  parameters:
  - `moisture_percent` (parameter: "moisture")
  - `ash_percent` (parameter: "ash")
  - `lignin_percent` (parameter: "lignin")
- **Analytical Flags:** `Boolean` flags indicating existence of:
  - `has_compositional`, `has_proximate`, `has_ultimate`, `has_xrf`, `has_icp`,
    `has_calorimetry`, `has_xrd`, `has_ftnir`.
  - `has_fermentation`, `has_gasification`.
- **Volume Metrics:** `total_annual_volume` (sum of production) and
  `county_count` from `BillionTon2023Record`.
- **Search Vector:** Pre-compute `tsvector` for name, description, and
  classifications.
- **Tags (PHASE 2):** Derivation of descriptors based on summary statistics
  (e.g., "high sugar" for top 10% glucose+xylose). _This will be implemented
  after the core metrics are validated._

### 2.2 `mv_biomass_composition`

- **Grain:** One row per `resource` × `parameter` × `analysis_type`.
- **Revisions:** Expand the `union_all` to include `XrdRecord` and
  `FtnirRecord`.

### 2.3 `mv_biomass_county_production`

- **Grain:** One row per `resource` × `county` × `scenario`.
- **Revisions:** Map the following fields from `BillionTon2023Record`:
  - `price_offered_usd`
  - `production_energy_content` (label: `energy_content`)
  - `product_density_dtpersqmi` (label: `density_dt_per_sqmi`)
  - `county_square_miles`

### 2.4 `mv_biomass_fermentation`

- **Grain:** One row per `resource` × `strain` × `pretreatment` × `enzyme` ×
  `product`.
- **Revisions:**
  - Join `fermentation_record.pretreatment_method_id` to `Method.name` as
    `pretreatment_method`.
  - Join `fermentation_record.eh_method_id` to `Method.name` as `enzyme_name`.
  - Include `unit` label from `Unit` table.

### 2.5 `mv_biomass_gasification`

- **Grain:** One row per `resource` × `reactor_type` × `parameter`.
- **Revisions:**
  - Pull `bed_temperature` and `gas_flow_rate` directly from
    `GasificationRecord`.
  - Include `unit` label from `Unit` table.

### 2.6 `mv_biomass_sample_stats`

- **Grain:** One row per `resource`.
- **Revisions:**
  - Join `PreparedSample` → `FieldSample` → `Provider` to calculate
    `supplier_count` (unique providers).

### 2.7 `mv_biomass_availability`

- **Revisions:**
  - Ensure residue factors are named `dry_tons_per_acre` and
    `wet_tons_per_acre`.

## 3. Exclusions

- **`mv_biomass_pricing`**: This view is deferred for future implementation as
  the source price columns in `UsdaMarketRecord` require further verification.

## 4. Performance Optimization

- Implement `UNIQUE` indexes on primary keys for `REFRESH CONCURRENTLY`.
- Add `GIN` indexes on `mv_biomass_search` for `name` (trigram) and
  `search_vector`.
- Add `B-tree` indexes on `resource_id` across all views.

## 5. Execution Steps

1. Update `Resource` model to include `uri` column.
2. Generate and apply migration for `Resource.uri`.
3. Modify `data_portal_views.py` with revised SQLAlchemy Core expressions.
4. Update `refresh_all_views()` logic if necessary.
5. Apply changes via Alembic migration (`pixi run migrate-autogenerate`).
6. Validate view contents against the PDF specification.

## 6. Implementation Summary (Completed 2026-03-16)

### 6.1 Model & Migration

- Added `uri` field to `Resource` model.
- Successfully applied migration `23a53daf6d9f` (Add uri to resource).
- Successfully applied migration `5f14811d264f`, `9fe87687000a`, `fabb4602bbe0`,
  and `6a7d2cde4f41` for view logic and optimizations.

### 6.2 View Logic Revisions

- **`mv_biomass_search`**: Fully implemented with moisture/sugar/ash/lignin
  averages, existence flags, seasonality, and full-text search vector.
- **`mv_biomass_composition`**: Expanded to 8 analysis types (including
  XRD/FTNIR).
- **`mv_biomass_sample_stats`**: Accurate distinct counts for samples, datasets,
  and suppliers across all 10 record types.
- **`mv_biomass_county_production`**: Includes all Billion Ton 2023 scenario
  metrics.
- **`mv_biomass_fermentation`**: Joins experimental metadata from `Method` and
  `Strain` tables.
- **`mv_biomass_gasification`**: Includes reactor-specific telemetry.

### 6.3 Performance & Indexing

- **Concurrent Refresh Support**: All views now have a unique `id` column
  (row_number() or PK) with a `UNIQUE` index.
- **Search Optimization**: `mv_biomass_search` includes a GIN index on `name`
  (trigram) and `search_vector`.
- **Row Counts (Current State)**:
  - `mv_biomass_search`: 115 rows
  - `mv_biomass_sample_stats`: 115 rows
  - `mv_biomass_county_production`: ~10,000 rows
  - `mv_biomass_fermentation`: 0 rows (Flagged: pending observation data
    mapping)

### 6.4 Follow-up Items (Flags)

- **Pretreatment Integration**: Need to incorporate specific values from the
  `pretreatment_record` table into the characterization or bioconversion views.
- **Fermentation Data Gap**: Investigate why `mv_biomass_fermentation` is empty
  despite 231 source records (check `observation` table `record_type` mapping).
- **Phase 2 Tags**: Implement the percentile-based array column for resource
  descriptors.
- **Pricing View**: Implement `mv_biomass_pricing` once the `UsdaMarketRecord`
  schema is finalized.
