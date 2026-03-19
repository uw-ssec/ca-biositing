-- Seed place table with California state + target counties for ETL pipelines.
-- These are also seeded by Alembic migration a085cd4a462e; this script is
-- provided for convenience when bootstrapping a test database manually.

INSERT INTO place (geoid, state_name, state_fips, county_name, county_fips, agg_level_desc)
VALUES
  ('06000', 'california', '06', NULL, '000', 'STATE'),
  ('06077', 'california', '06', 'san joaquin', '077', 'COUNTY'),
  ('06099', 'california', '06', 'stanislaus', '099', 'COUNTY'),
  ('06047', 'california', '06', 'merced', '047', 'COUNTY')
ON CONFLICT (geoid) DO UPDATE SET
  state_name = EXCLUDED.state_name,
  county_name = EXCLUDED.county_name;

-- Verify seeding
SELECT geoid, state_name, county_name, agg_level_desc
FROM place
WHERE geoid IN ('06000', '06077', '06099', '06047')
ORDER BY geoid;
