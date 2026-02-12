--
-- Name: usda_census_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

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
