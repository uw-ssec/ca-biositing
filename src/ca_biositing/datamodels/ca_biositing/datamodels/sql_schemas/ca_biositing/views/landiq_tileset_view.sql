--
-- Name: landiq_tileset_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

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
