-- Seed place table with California state + target counties for ETL pipelines.
-- These are also seeded by Alembic migration a085cd4a462e; this script is
-- provided for convenience when bootstrapping a test database manually.

INSERT INTO place (geoid, state_name, state_fips, county_name, county_fips, agg_level_desc)
VALUES
  ('06000', 'CALIFORNIA', '06', NULL, '000', 'STATE'),
  ('06077', 'CALIFORNIA', '06', 'SAN JOAQUIN', '077', 'COUNTY'),
  ('06099', 'CALIFORNIA', '06', 'STANISLAUS', '099', 'COUNTY'),
  ('06047', 'CALIFORNIA', '06', 'MERCED', '047', 'COUNTY')
ON CONFLICT (geoid) DO NOTHING;

-- Verify seeding
SELECT geoid, state_name, county_name, agg_level_desc
FROM place
WHERE geoid IN ('06000', '06077', '06099', '06047')
ORDER BY geoid;
