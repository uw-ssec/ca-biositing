# Data Portal Views - Raw SQL Reference

This document contains the compiled SQL for all materialized views in the data
portal.

**Purpose**: When creating migrations with raw SQL snapshots, copy the SQL from
this reference file and embed it directly in your migration file using the
pattern from [`alembic/AGENTS.md`](./AGENTS.md).

**Generated**: 2026-04-04

---

## mv_biomass_search

**Schema**: `data_portal.mv_biomass_search`

**Purpose**: Comprehensive biomass search view combining resource metadata,
analytical metrics, availability data, and supply volume projections.

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)
```

**SQL**:

```sql
SELECT resource.id, resource.name, resource.resource_code, resource.description, resource_class.name AS resource_class, resource_subclass.name AS resource_subclass, primary_ag_product.name AS primary_product, resource_morphology.morphology_uri AS image_url, resource.uri AS literature_uri, anon_1.total_annual_volume, anon_1.county_count, anon_1.volume_unit, anon_2.moisture_percent, anon_2.sugar_content_percent, anon_2.ash_percent, anon_2.lignin_percent, anon_2.carbon_percent, anon_2.hydrogen_percent, anon_2.cn_ratio, coalesce(anon_3.tags, CAST(ARRAY[] AS VARCHAR[])) AS tags, anon_4.from_month AS season_from_month, anon_4.to_month AS season_to_month, anon_4.year_round, coalesce(anon_2.has_proximate, false) AS has_proximate, coalesce(anon_2.has_compositional, false) AS has_compositional, coalesce(anon_2.has_ultimate, false) AS has_ultimate, coalesce(anon_2.has_xrf, false) AS has_xrf, coalesce(anon_2.has_icp, false) AS has_icp, coalesce(anon_2.has_calorimetry, false) AS has_calorimetry, coalesce(anon_2.has_xrd, false) AS has_xrd, coalesce(anon_2.has_ftnir, false) AS has_ftnir, coalesce(anon_2.has_fermentation, false) AS has_fermentation, coalesce(anon_2.has_gasification, false) AS has_gasification, coalesce(anon_2.has_pretreatment, false) AS has_pretreatment, CASE WHEN (anon_2.moisture_percent IS NOT NULL) THEN true ELSE false END AS has_moisture_data, CASE WHEN (anon_2.sugar_content_percent > 0) THEN true ELSE false END AS has_sugar_data, CASE WHEN (resource_morphology.morphology_uri IS NOT NULL) THEN true ELSE false END AS has_image, CASE WHEN (anon_1.total_annual_volume IS NOT NULL) THEN true ELSE false END AS has_volume_data, resource.created_at, resource.updated_at, to_tsvector('english', coalesce(resource.name, '') || ' ' || coalesce(resource.description, '') || ' ' || coalesce(resource_class.name, '') || ' ' || coalesce(resource_subclass.name, '') || ' ' || coalesce(primary_ag_product.name, '')) AS search_vector FROM resource LEFT OUTER JOIN resource_class ON resource.resource_class_id = resource_class.id LEFT OUTER JOIN resource_subclass ON resource.resource_subclass_id = resource_subclass.id LEFT OUTER JOIN primary_ag_product ON resource.primary_ag_product_id = primary_ag_product.id LEFT OUTER JOIN resource_morphology ON resource_morphology.resource_id = resource.id LEFT OUTER JOIN (SELECT billion_ton2023_record.resource_id AS resource_id, sum(billion_ton2023_record.production) AS total_annual_volume, count(distinct(billion_ton2023_record.geoid)) AS county_count, max(unit.name) AS volume_unit FROM billion_ton2023_record JOIN unit ON billion_ton2023_record.production_unit_id = unit.id GROUP BY billion_ton2023_record.resource_id) AS anon_1 ON anon_1.resource_id = resource.id LEFT OUTER JOIN (SELECT anon_5.resource_id AS resource_id, avg(CASE WHEN (anon_6.parameter = 'moisture') THEN anon_6.value END) AS moisture_percent, avg(CASE WHEN (anon_6.parameter = 'ash') THEN anon_6.value END) AS ash_percent, CASE WHEN (avg(CASE WHEN (anon_6.parameter = 'lignin') THEN anon_6.value END) IS NOT NULL OR avg(CASE WHEN (anon_6.parameter = 'lignin+') THEN anon_6.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_6.parameter = 'lignin') THEN anon_6.value END), 0) + coalesce(avg(CASE WHEN (anon_6.parameter = 'lignin+') THEN anon_6.value END), 0) END AS lignin_percent, CASE WHEN (avg(CASE WHEN (anon_6.parameter = 'glucose') THEN anon_6.value END) IS NOT NULL OR avg(CASE WHEN (anon_6.parameter = 'xylose') THEN anon_6.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_6.parameter = 'glucose') THEN anon_6.value END), 0) + coalesce(avg(CASE WHEN (anon_6.parameter = 'xylose') THEN anon_6.value END), 0) END AS sugar_content_percent, avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'carbon') THEN anon_6.value END) AS carbon_percent, avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'hydrogen') THEN anon_6.value END) AS hydrogen_percent, CASE WHEN (avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'carbon') THEN anon_6.value END) IS NOT NULL AND avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'nitrogen') THEN anon_6.value END) IS NOT NULL AND avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'nitrogen') THEN anon_6.value END) != 0) THEN avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'carbon') THEN anon_6.value END) / CAST(avg(CASE WHEN (anon_5.type = 'ultimate analysis' AND lower(anon_6.parameter) = 'nitrogen') THEN anon_6.value END) AS NUMERIC) END AS cn_ratio, bool_or(anon_5.type = 'proximate analysis') AS has_proximate, bool_or(anon_5.type = 'compositional analysis') AS has_compositional, bool_or(anon_5.type = 'ultimate analysis') AS has_ultimate, bool_or(anon_5.type = 'xrf analysis') AS has_xrf, bool_or(anon_5.type = 'icp analysis') AS has_icp, bool_or(anon_5.type = 'calorimetry analysis') AS has_calorimetry, bool_or(anon_5.type = 'xrd analysis') AS has_xrd, bool_or(anon_5.type = 'ftnir analysis') AS has_ftnir, bool_or(anon_5.type = 'fermentation') AS has_fermentation, bool_or(anon_5.type = 'gasification') AS has_gasification, bool_or(anon_5.type = 'pretreatment') AS has_pretreatment FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_5 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_6 ON anon_5.resource_id = anon_6.record_id AND anon_5.type = anon_6.record_type GROUP BY anon_5.resource_id) AS anon_2 ON anon_2.resource_id = resource.id LEFT OUTER JOIN (SELECT anon_7.resource_id, func.array_remove(pg_array([CASE WHEN (anon_7.moisture_percent <= (SELECT percentile_cont(0.1) WITHIN GROUP (ORDER BY anon_8.moisture_percent) FROM (SELECT anon_9.resource_id, avg(CASE WHEN (anon_10.parameter = 'moisture') THEN anon_10.value END) AS moisture_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_9 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_10 ON anon_9.resource_id = anon_10.record_id AND anon_9.type = anon_10.record_type GROUP BY anon_9.resource_id) AS anon_8) THEN 'low moisture' END, CASE WHEN (anon_7.moisture_percent >= (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY anon_11.moisture_percent) FROM (SELECT anon_12.resource_id, avg(CASE WHEN (anon_13.parameter = 'moisture') THEN anon_13.value END) AS moisture_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_12 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_13 ON anon_12.resource_id = anon_13.record_id AND anon_12.type = anon_13.record_type GROUP BY anon_12.resource_id) AS anon_11) THEN 'high moisture' END, CASE WHEN (anon_7.ash_percent <= (SELECT percentile_cont(0.1) WITHIN GROUP (ORDER BY anon_14.ash_percent) FROM (SELECT anon_15.resource_id, avg(CASE WHEN (anon_16.parameter = 'ash') THEN anon_16.value END) AS ash_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_15 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_16 ON anon_15.resource_id = anon_16.record_id AND anon_15.type = anon_16.record_type GROUP BY anon_15.resource_id) AS anon_14) THEN 'low ash' END, CASE WHEN (anon_7.ash_percent >= (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY anon_17.ash_percent) FROM (SELECT anon_18.resource_id, avg(CASE WHEN (anon_19.parameter = 'ash') THEN anon_19.value END) AS ash_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_18 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_19 ON anon_18.resource_id = anon_19.record_id AND anon_18.type = anon_19.record_type GROUP BY anon_18.resource_id) AS anon_17) THEN 'high ash' END, CASE WHEN (anon_7.lignin_percent <= (SELECT percentile_cont(0.1) WITHIN GROUP (ORDER BY anon_20.lignin_percent) FROM (SELECT anon_21.resource_id, CASE WHEN (avg(CASE WHEN (anon_22.parameter = 'lignin') THEN anon_22.value END) IS NOT NULL OR avg(CASE WHEN (anon_22.parameter = 'lignin+') THEN anon_22.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_22.parameter = 'lignin') THEN anon_22.value END), 0) + coalesce(avg(CASE WHEN (anon_22.parameter = 'lignin+') THEN anon_22.value END), 0) END AS lignin_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_21 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_22 ON anon_21.resource_id = anon_22.record_id AND anon_21.type = anon_22.record_type GROUP BY anon_21.resource_id) AS anon_20) THEN 'low lignin' END, CASE WHEN (anon_7.lignin_percent >= (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY anon_23.lignin_percent) FROM (SELECT anon_24.resource_id, CASE WHEN (avg(CASE WHEN (anon_25.parameter = 'lignin') THEN anon_25.value END) IS NOT NULL OR avg(CASE WHEN (anon_25.parameter = 'lignin+') THEN anon_25.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_25.parameter = 'lignin') THEN anon_25.value END), 0) + coalesce(avg(CASE WHEN (anon_25.parameter = 'lignin+') THEN anon_25.value END), 0) END AS lignin_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_24 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_25 ON anon_24.resource_id = anon_25.record_id AND anon_24.type = anon_25.record_type GROUP BY anon_24.resource_id) AS anon_23) THEN 'high lignin' END, CASE WHEN (anon_7.sugar_content_percent <= (SELECT percentile_cont(0.1) WITHIN GROUP (ORDER BY anon_26.sugar_content_percent) FROM (SELECT anon_27.resource_id, CASE WHEN (avg(CASE WHEN (anon_28.parameter = 'glucose') THEN anon_28.value END) IS NOT NULL OR avg(CASE WHEN (anon_28.parameter = 'xylose') THEN anon_28.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_28.parameter = 'glucose') THEN anon_28.value END), 0) + coalesce(avg(CASE WHEN (anon_28.parameter = 'xylose') THEN anon_28.value END), 0) END AS sugar_content_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_27 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_28 ON anon_27.resource_id = anon_28.record_id AND anon_27.type = anon_28.record_type GROUP BY anon_27.resource_id) AS anon_26) THEN 'low sugar' END, CASE WHEN (anon_7.sugar_content_percent >= (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY anon_29.sugar_content_percent) FROM (SELECT anon_30.resource_id, CASE WHEN (avg(CASE WHEN (anon_31.parameter = 'glucose') THEN anon_31.value END) IS NOT NULL OR avg(CASE WHEN (anon_31.parameter = 'xylose') THEN anon_31.value END) IS NOT NULL) THEN coalesce(avg(CASE WHEN (anon_31.parameter = 'glucose') THEN anon_31.value END), 0) + coalesce(avg(CASE WHEN (anon_31.parameter = 'xylose') THEN anon_31.value END), 0) END AS sugar_content_percent FROM (SELECT resource_analysis_map.resource_id, resource_analysis_map.type FROM resource_analysis_map) AS anon_30 LEFT OUTER JOIN (SELECT observation.record_id, lower(observation.record_id) AS lower_1, observation.record_type, observation.value, parameter.name AS parameter FROM observation JOIN parameter ON observation.parameter_id = parameter.id) AS anon_31 ON anon_30.resource_id = anon_31.record_id AND anon_30.type = anon_31.record_type GROUP BY anon_30.resource_id) AS anon_29) THEN 'high sugar' END]), NULL) AS tags FROM anon_7) AS anon_3 ON anon_3.resource_id = resource.id LEFT OUTER JOIN (SELECT resource_availability.resource_id, min(resource_availability.from_month) AS from_month, max(resource_availability.to_month) AS to_month, bool_or(resource_availability.year_round) AS year_round FROM resource_availability GROUP BY resource_availability.resource_id) AS anon_4 ON anon_4.resource_id = resource.id
```

---

## mv_biomass_availability

**Schema**: `data_portal.mv_biomass_availability`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_availability_id ON data_portal.mv_biomass_availability (id)
```

**SQL**:

```sql
SELECT resource.id AS resource_id, resource.name AS resource_name, min(resource_availability.from_month) AS from_month, max(resource_availability.to_month) AS to_month, bool_or(resource_availability.year_round) AS year_round, avg(resource_availability.residue_factor_dry_tons_acre) AS dry_tons_per_acre, avg(resource_availability.residue_factor_wet_tons_acre) AS wet_tons_per_acre FROM resource_availability JOIN resource ON resource_availability.resource_id = resource.id GROUP BY resource.id, resource.name
```

---

## mv_biomass_composition

**Schema**: `data_portal.mv_biomass_composition`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)
```

**SQL**: See `scripts/extract_view_sql.py` output for complete SQL (very long
query with multiple CTEs)

---

## mv_biomass_county_production

**Schema**: `data_portal.mv_biomass_county_production`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_county_production_id ON data_portal.mv_biomass_county_production (id)
```

**SQL**: See `scripts/extract_view_sql.py` output for complete SQL

---

## mv_biomass_sample_stats

**Schema**: `data_portal.mv_biomass_sample_stats`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_id ON data_portal.mv_biomass_sample_stats (id)
```

**SQL**: See `scripts/extract_view_sql.py` output for complete SQL

---

## mv_biomass_fermentation

**Schema**: `data_portal.mv_biomass_fermentation`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)
```

**SQL**:

```sql
SELECT row_number() OVER (ORDER BY fermentation_record.resource_id, strain.name, pm.name, em.name, parameter.name, unit.name) AS id, fermentation_record.resource_id, resource.name AS resource_name, strain.name AS strain_name, pm.name AS pretreatment_method, em.name AS enzyme_name, parameter.name AS product_name, avg(observation.value) AS avg_value, min(observation.value) AS min_value, max(observation.value) AS max_value, stddev(observation.value) AS std_dev, count(*) AS observation_count, unit.name AS unit FROM fermentation_record JOIN resource ON fermentation_record.resource_id = resource.id LEFT OUTER JOIN strain ON fermentation_record.strain_id = strain.id LEFT OUTER JOIN method AS pm ON fermentation_record.pretreatment_method_id = pm.id LEFT OUTER JOIN method AS em ON fermentation_record.eh_method_id = em.id JOIN observation ON lower(observation.record_id) = lower(fermentation_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id GROUP BY fermentation_record.resource_id, resource.name, strain.name, pm.name, em.name, parameter.name, unit.name
```

---

## mv_biomass_gasification

**Schema**: `data_portal.mv_biomass_gasification`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)
```

**SQL**:

```sql
SELECT row_number() OVER (ORDER BY gasification_record.resource_id, decon_vessel.name, parameter.name, unit.name) AS id, gasification_record.resource_id, resource.name AS resource_name, decon_vessel.name AS reactor_type, parameter.name AS parameter_name, avg(observation.value) AS avg_value, min(observation.value) AS min_value, max(observation.value) AS max_value, stddev(observation.value) AS std_dev, count(*) AS observation_count, unit.name AS unit FROM gasification_record JOIN resource ON gasification_record.resource_id = resource.id LEFT OUTER JOIN decon_vessel ON gasification_record.reactor_type_id = decon_vessel.id JOIN observation ON lower(observation.record_id) = lower(gasification_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id GROUP BY gasification_record.resource_id, resource.name, decon_vessel.name, parameter.name, unit.name
```

---

## mv_biomass_pricing

**Schema**: `data_portal.mv_biomass_pricing`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_biomass_pricing_id ON data_portal.mv_biomass_pricing (id)
```

**SQL**:

```sql
SELECT row_number() OVER (ORDER BY usda_market_record.id) AS id, usda_commodity.name AS commodity_name, place.geoid, place.county_name AS county, place.state_name AS state, usda_market_record.report_date, usda_market_record.market_type_category, usda_market_record.sale_type, anon_1.price_min, anon_1.price_max, anon_1.price_avg, anon_1.price_unit FROM usda_market_record JOIN usda_market_report ON usda_market_record.report_id = usda_market_report.id JOIN usda_commodity ON usda_market_record.commodity_id = usda_commodity.id LEFT OUTER JOIN location_address ON usda_market_report.office_city_id = location_address.id LEFT OUTER JOIN place ON location_address.geography_id = place.geoid JOIN (SELECT observation.record_id AS record_id, avg(observation.value) AS price_avg, min(observation.value) AS price_min, max(observation.value) AS price_max, unit.name AS price_unit FROM observation JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id WHERE observation.record_type = 'usda_market_record' AND lower(parameter.name) = 'price received' GROUP BY observation.record_id, unit.name) AS anon_1 ON CAST(usda_market_record.id AS VARCHAR) = anon_1.record_id
```

---

## mv_usda_county_production

**Schema**: `data_portal.mv_usda_county_production`

**Index Required**:

```sql
CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)
```

**SQL**: See `scripts/extract_view_sql.py` output for complete SQL (very long
query with multiple CTEs)

---

## How to Use This Reference

When creating a migration to update a view:

1. Run: `pixi run python scripts/extract_view_sql.py`
2. Copy the SQL for your view from that output (or from this reference file)
3. Embed it in your migration following the template in
   [`alembic/AGENTS.md`](./AGENTS.md)
4. Example:

```python
def upgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_pricing CASCADE")

    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_pricing AS
        SELECT row_number() OVER (...) AS id, ...
    """)

    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_pricing_id
        ON data_portal.mv_biomass_pricing (id)
    """)

    op.execute("GRANT SELECT ON data_portal.mv_biomass_pricing TO biocirv_readonly")
```

---

## Notes

- This reference file is manually maintained. If view SQL changes, regenerate it
  via:

  ```bash
  pixi run python scripts/extract_view_sql.py > alembic/VIEW_SQL_REFERENCE.md
  ```

- Long queries (mv_biomass_composition, mv_biomass_county_production, etc.) are
  truncated above. Use the extraction script to get the full SQL.

- Each SQL string should be copied exactly as output by the SQLAlchemy compiler.
  Avoid manual reformatting to ensure consistency across replays.
