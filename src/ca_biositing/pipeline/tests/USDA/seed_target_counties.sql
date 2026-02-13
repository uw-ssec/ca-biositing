-- Seed place table with target counties for USDA ETL
-- North San Joaquin Valley counties: San Joaquin, Stanislaus, Merced

INSERT INTO place (geoid, state_name, state_fips, county_name, county_fips, agg_level_desc)
VALUES
  ('06077', 'CALIFORNIA', '06', 'SAN JOAQUIN', '077', 'COUNTY'),
  ('06099', 'CALIFORNIA', '06', 'STANISLAUS', '099', 'COUNTY'),
  ('06047', 'CALIFORNIA', '06', 'MERCED', '047', 'COUNTY')
ON CONFLICT (geoid) DO NOTHING;

-- Verify seeding
SELECT geoid, state_name, county_name
FROM place
WHERE geoid IN ('06077', '06099', '06047')
ORDER BY geoid;
