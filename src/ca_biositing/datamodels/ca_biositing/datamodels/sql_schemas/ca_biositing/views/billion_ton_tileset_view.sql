--
-- Name: billion_ton_tileset_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

CREATE MATERIALIZED VIEW ca_biositing.billion_ton_tileset_view AS
SELECT
  btr.id,
  r.name as resource,
  p.county_name as county,
  'production'::text as parameter,
  btr.production::float as value,
  u.name as unit,
  btr.etl_run_id as tileset_id
FROM public.billion_ton2023_record btr
JOIN public.resource r ON btr.resource_id = r.id
JOIN public.place p ON btr.geoid = p.geoid
JOIN public.unit u ON btr.production_unit_id = u.id;
