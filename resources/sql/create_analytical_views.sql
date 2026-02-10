-- Analytical Layer Views
-- This script creates materialized views in the ca_biositing schema.

-- Initial View: landiq_record_view
-- Combines record metadata with polygon geometry.
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.landiq_record_view;

CREATE MATERIALIZED VIEW ca_biositing.landiq_record_view AS
SELECT
  lr.record_id,
  p.geom::geometry as geom,
  p.geoid,
  pap.name as crop_name,
  lr.acres,
  lr.irrigated,
  lr.confidence,
  lr.dataset_id
FROM public.landiq_record lr
JOIN public.polygon p ON lr.polygon_id = p.id
JOIN public.primary_ag_product pap ON lr.main_crop = pap.id;

-- Index for spatial performance
CREATE INDEX IF NOT EXISTS idx_landiq_record_view_geom ON ca_biositing.landiq_record_view USING GIST (geom);

-- View: analysis_data_view
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.analysis_data_view;

CREATE MATERIALIZED VIEW ca_biositing.analysis_data_view AS
SELECT
  obs.id,
  res.name as resource,
  '06000'::text as geoid,
  param.name as parameter,
  obs.value,
  u.name as unit
FROM public.observation obs
JOIN public.parameter param ON obs.parameter_id = param.id
JOIN public.unit u ON obs.unit_id = u.id
LEFT JOIN public.proximate_record pr ON obs.record_id = pr.record_id AND obs.record_type = 'proximate analysis'
LEFT JOIN public.ultimate_record ur ON obs.record_id = ur.record_id AND obs.record_type = 'ultimate analysis'
LEFT JOIN public.compositional_record cr ON obs.record_id = cr.record_id AND obs.record_type = 'compositional analysis'
LEFT JOIN public.icp_record ir ON obs.record_id = ir.record_id AND obs.record_type = 'icp analysis'
LEFT JOIN public.prepared_sample ps ON ps.id = COALESCE(pr.prepared_sample_id, ur.prepared_sample_id, cr.prepared_sample_id, ir.prepared_sample_id)
LEFT JOIN public.field_sample fs ON fs.id = ps.field_sample_id
LEFT JOIN public.resource res ON res.id = fs.resource_id;

-- View: landiq_tileset_view
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.landiq_tileset_view;

CREATE MATERIALIZED VIEW ca_biositing.landiq_tileset_view AS
SELECT
  lr.id,
  p.geom::geometry as geom,
  pap.name as main_crop,
  lr.acres,
  lr.county,
  p.geoid,
  lr.dataset_id as tileset_id
FROM public.landiq_record lr
JOIN public.polygon p ON lr.polygon_id = p.id
JOIN public.primary_ag_product pap ON lr.main_crop = pap.id;

-- Index for spatial performance
CREATE INDEX IF NOT EXISTS idx_landiq_tileset_view_geom ON ca_biositing.landiq_tileset_view USING GIST (geom);

-- View: usda_census_view
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.usda_census_view;

CREATE MATERIALIZED VIEW ca_biositing.usda_census_view AS
SELECT
  obs.id,
  uc.name as usda_crop,
  p.geoid,
  param.name as parameter,
  obs.value,
  u.name as unit,
  dt.name as dimension,
  obs.dimension_value,
  du.name as dimension_unit
FROM public.observation obs
JOIN public.usda_census_record ucr ON obs.record_id = ucr.id::text AND obs.record_type = 'usda_census_record'
JOIN public.usda_commodity uc ON ucr.commodity_code = uc.id
JOIN public.place p ON ucr.geoid = p.geoid
JOIN public.parameter param ON obs.parameter_id = param.id
JOIN public.unit u ON obs.unit_id = u.id
LEFT JOIN public.dimension_type dt ON obs.dimension_type_id = dt.id
LEFT JOIN public.unit du ON obs.dimension_unit_id = du.id;

-- View: analysis_average_view
-- Aggregates analysis data by resource, location, and parameter.
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.analysis_average_view;

CREATE MATERIALIZED VIEW ca_biositing.analysis_average_view AS
SELECT
  resource,
  geoid,
  parameter,
  AVG(value) as average_value,
  unit,
  COUNT(*) as observation_count
FROM ca_biositing.analysis_data_view
GROUP BY resource, geoid, parameter, unit;

-- View: usda_survey_view
DROP MATERIALIZED VIEW IF EXISTS ca_biositing.usda_survey_view;

CREATE MATERIALIZED VIEW ca_biositing.usda_survey_view AS
SELECT
  obs.id,
  uc.name as usda_crop,
  p.geoid,
  param.name as parameter,
  obs.value,
  u.name as unit,
  dt.name as dimension,
  obs.dimension_value,
  du.name as dimension_unit
FROM public.observation obs
JOIN public.usda_survey_record usr ON obs.record_id = usr.id::text AND obs.record_type = 'usda_survey_record'
JOIN public.usda_commodity uc ON usr.commodity_code = uc.id
JOIN public.place p ON usr.geoid = p.geoid
JOIN public.parameter param ON obs.parameter_id = param.id
JOIN public.unit u ON obs.unit_id = u.id
LEFT JOIN public.dimension_type dt ON obs.dimension_type_id = dt.id
LEFT JOIN public.unit du ON obs.dimension_unit_id = du.id;
