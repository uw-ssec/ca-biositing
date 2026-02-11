--
-- Name: analysis_data_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

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
