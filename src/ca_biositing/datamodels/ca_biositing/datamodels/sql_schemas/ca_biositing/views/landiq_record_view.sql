--
-- Name: landiq_record_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

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
