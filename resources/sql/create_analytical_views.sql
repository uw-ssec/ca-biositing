-- [GENERATED] Materialized view definitions for ca_biositing schema
-- DO NOT EDIT MANUALLY. Matches Python definitions in src/ca_biositing/datamodels/ca_biositing/datamodels/views.py

CREATE SCHEMA IF NOT EXISTS ca_biositing;

-- 1. landiq_record_view
CREATE MATERIALIZED VIEW ca_biositing.landiq_record_view AS
SELECT
    lr.record_id,
    p.geom,
    p.geoid,
    pap.name AS crop_name,
    lr.acres,
    lr.irrigated,
    lr.confidence,
    lr.dataset_id
FROM landiq_record lr
JOIN polygon p ON lr.polygon_id = p.id
JOIN primary_ag_product pap ON lr.main_crop = pap.id;

-- 2. landiq_tileset_view
CREATE MATERIALIZED VIEW ca_biositing.landiq_tileset_view AS
SELECT
    lr.id,
    p.geom,
    pap.name AS main_crop,
    lr.acres,
    lr.county,
    p.geoid,
    lr.dataset_id AS tileset_id
FROM landiq_record lr
JOIN polygon p ON lr.polygon_id = p.id
JOIN primary_ag_product pap ON lr.main_crop = pap.id;

-- 3. analysis_data_view
-- NOTE: This view must be refreshed BEFORE ca_biositing.analysis_average_view
CREATE MATERIALIZED VIEW ca_biositing.analysis_data_view AS
SELECT
    obs.id,
    obs.record_id,
    obs.record_type,
    res.id AS resource_id,
    res.name AS resource,
    la.geography_id AS geoid,
    param.name AS parameter,
    obs.value,
    u.name AS unit,
    dt.name AS dimension,
    obs.dimension_value,
    du.name AS dimension_unit
FROM observation obs
JOIN parameter param ON obs.parameter_id = param.id
JOIN unit u ON obs.unit_id = u.id
LEFT JOIN dimension_type dt ON obs.dimension_type_id = dt.id
LEFT JOIN unit du ON obs.dimension_unit_id = du.id
LEFT JOIN proximate_record pr ON obs.record_id = pr.record_id AND obs.record_type = 'proximate analysis'
LEFT JOIN ultimate_record ur ON obs.record_id = ur.record_id AND obs.record_type = 'ultimate analysis'
LEFT JOIN compositional_record cr ON obs.record_id = cr.record_id AND obs.record_type = 'compositional analysis'
LEFT JOIN icp_record ir ON obs.record_id = ir.record_id AND (obs.record_type = 'icp analysis' OR obs.record_type = 'icp-oes' OR obs.record_type = 'icp-ms')
LEFT JOIN xrf_record xr ON obs.record_id = xr.record_id AND obs.record_type = 'xrf analysis'
LEFT JOIN calorimetry_record calr ON obs.record_id = calr.record_id AND obs.record_type = 'calorimetry analysis'
LEFT JOIN xrd_record xrr ON obs.record_id = xrr.record_id AND obs.record_type = 'xrd analysis'
LEFT JOIN fermentation_record fr ON obs.record_id = fr.record_id AND obs.record_type = 'fermentation'
LEFT JOIN pretreatment_record ptr ON obs.record_id = ptr.record_id AND obs.record_type = 'pretreatment'
LEFT JOIN prepared_sample ps ON ps.id = COALESCE(
    pr.prepared_sample_id, ur.prepared_sample_id, cr.prepared_sample_id, ir.prepared_sample_id,
    xr.prepared_sample_id, calr.prepared_sample_id, xrr.prepared_sample_id, fr.prepared_sample_id,
    ptr.prepared_sample_id
)
LEFT JOIN field_sample fs ON fs.id = ps.field_sample_id
LEFT JOIN resource res ON res.id = COALESCE(
    pr.resource_id, ur.resource_id, cr.resource_id, ir.resource_id,
    xr.resource_id, calr.resource_id, xrr.resource_id, fr.resource_id, ptr.resource_id,
    fs.resource_id
)
LEFT JOIN location_address la ON fs.sampling_location_id = la.id
WHERE obs.record_type NOT IN ('usda_census_record', 'usda_survey_record');

-- 4. usda_census_view (V1)
CREATE MATERIALIZED VIEW ca_biositing.usda_census_view AS
SELECT
    obs.id,
    uc.name AS usda_crop,
    p.geoid,
    param.name AS parameter,
    obs.value,
    u.name AS unit,
    dt.name AS dimension,
    obs.dimension_value,
    du.name AS dimension_unit
FROM observation obs
JOIN usda_census_record ucr ON obs.record_id = CAST(ucr.id AS text) AND obs.record_type = 'usda_census_record'
JOIN usda_commodity uc ON ucr.commodity_code = uc.id
JOIN place p ON ucr.geoid = p.geoid
JOIN parameter param ON obs.parameter_id = param.id
JOIN unit u ON obs.unit_id = u.id
LEFT JOIN dimension_type dt ON obs.dimension_type_id = dt.id
LEFT JOIN unit du ON obs.dimension_unit_id = du.id;

-- 5. usda_survey_view (V1)
CREATE MATERIALIZED VIEW ca_biositing.usda_survey_view AS
SELECT
    obs.id,
    uc.name AS usda_crop,
    p.geoid,
    param.name AS parameter,
    obs.value,
    u.name AS unit,
    dt.name AS dimension,
    obs.dimension_value,
    du.name AS dimension_unit
FROM observation obs
JOIN usda_survey_record usr ON obs.record_id = CAST(usr.id AS text) AND obs.record_type = 'usda_survey_record'
JOIN usda_commodity uc ON usr.commodity_code = uc.id
JOIN place p ON usr.geoid = p.geoid
JOIN parameter param ON obs.parameter_id = param.id
JOIN unit u ON obs.unit_id = u.id
LEFT JOIN dimension_type dt ON obs.dimension_type_id = dt.id
LEFT JOIN unit du ON obs.dimension_unit_id = du.id;

-- 6. billion_ton_tileset_view
CREATE MATERIALIZED VIEW ca_biositing.billion_ton_tileset_view AS
SELECT
    btr.id,
    r.name AS resource,
    p.county_name AS county,
    'production' AS parameter,
    btr.production::double precision AS value,
    u.name AS unit,
    btr.etl_run_id AS tileset_id
FROM billion_ton2023_record btr
JOIN resource r ON btr.resource_id = r.id
JOIN place p ON btr.geoid = p.geoid
JOIN unit u ON btr.production_unit_id = u.id;

-- 7. analysis_average_view
CREATE MATERIALIZED VIEW ca_biositing.analysis_average_view AS
SELECT resource, geoid, parameter,
       AVG(value) as average_value,
       STDDEV(value) as standard_deviation,
       unit, COUNT(*) as observation_count
FROM ca_biositing.analysis_data_view
GROUP BY resource, geoid, parameter, unit;

-- Spatial Indexes
CREATE INDEX IF NOT EXISTS idx_landiq_record_view_geom ON ca_biositing.landiq_record_view USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_landiq_tileset_view_geom ON ca_biositing.landiq_tileset_view USING GIST (geom);
