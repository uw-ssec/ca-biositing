--
-- Name: analysis_average_view; Type: MATERIALIZED VIEW; Schema: ca_biositing; Owner: -
--

CREATE MATERIALIZED VIEW ca_biositing.analysis_average_view AS
SELECT
  resource,
  geoid,
  parameter,
  AVG(value) as average_value,
  STDDEV(value) as standard_deviation,
  unit,
  COUNT(*) as observation_count
FROM ca_biositing.analysis_data_view
GROUP BY resource, geoid, parameter, unit;
