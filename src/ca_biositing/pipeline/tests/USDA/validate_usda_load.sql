-- Validate USDA ETL Load
-- Run after ETL completes to verify success

\echo ''
\echo '========================================'
\echo 'USDA ETL Validation Report'
\echo '========================================'

\echo ''
\echo '1️⃣  RECORD COUNTS'
\echo '---'
SELECT
  'Census Records' as record_type,
  COUNT(*) as count,
  COUNT(DISTINCT geoid) as unique_counties,
  COUNT(DISTINCT year) as unique_years
FROM usda_census_record
UNION ALL
SELECT
  'Survey Records',
  COUNT(*),
  COUNT(DISTINCT geoid),
  COUNT(DISTINCT year)
FROM usda_survey_record
UNION ALL
SELECT
  'Observations (total)',
  COUNT(*),
  COUNT(DISTINCT record_id),
  COUNT(DISTINCT (record_type))
FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record');

\echo ''
\echo '2️⃣  DATASET LINKAGE (Critical!)'
\echo '---'
SELECT
  'Census → Dataset' as linkage_check,
  COUNT(*) as total_records,
  COUNT(dataset_id) as with_dataset,
  COUNT(NULLIF(dataset_id, NULL)) as missing_dataset,
  ROUND(100.0 * COUNT(dataset_id) / COUNT(*), 1) as percent_linked
FROM usda_census_record
UNION ALL
SELECT
  'Survey → Dataset',
  COUNT(*),
  COUNT(dataset_id),
  COUNT(NULLIF(dataset_id, NULL)),
  ROUND(100.0 * COUNT(dataset_id) / COUNT(*), 1)
FROM usda_survey_record
UNION ALL
SELECT
  'Observations → Dataset',
  COUNT(*),
  COUNT(dataset_id),
  COUNT(NULLIF(dataset_id, NULL)),
  ROUND(100.0 * COUNT(dataset_id) / COUNT(*), 1)
FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record');

\echo ''
\echo '3️⃣  REFERENTIAL INTEGRITY (Foreign Keys)'
\echo '---'
SELECT
  'Census observations with valid parent' as integrity_check,
  COUNT(*) as total,
  SUM(CASE
    WHEN EXISTS (SELECT 1 FROM usda_census_record c WHERE c.id = observation.record_id::integer)
    THEN 1 ELSE 0
  END) as valid_parents,
  COUNT(*) - SUM(CASE
    WHEN EXISTS (SELECT 1 FROM usda_census_record c WHERE c.id = observation.record_id::integer)
    THEN 1 ELSE 0
  END) as orphaned
FROM observation
WHERE record_type = 'usda_census_record'
UNION ALL
SELECT
  'Survey observations with valid parent',
  COUNT(*),
  SUM(CASE
    WHEN EXISTS (SELECT 1 FROM usda_survey_record s WHERE s.id = observation.record_id::integer)
    THEN 1 ELSE 0
  END),
  COUNT(*) - SUM(CASE
    WHEN EXISTS (SELECT 1 FROM usda_survey_record s WHERE s.id = observation.record_id::integer)
    THEN 1 ELSE 0
  END)
FROM observation
WHERE record_type = 'usda_survey_record';

\echo ''
\echo '4️⃣  LINEAGE TRACKING (ETL Runs)'
\echo '---'
SELECT
  COUNT(DISTINCT etl_run_id) as distinct_etl_runs,
  COUNT(DISTINCT lineage_group_id) as distinct_lineage_groups,
  COUNT(DISTINCT created_at::date) as days_loaded,
  MIN(created_at) as first_record_time,
  MAX(created_at) as last_record_time
FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record');

\echo ''
\echo '5️⃣  DEDUPLICATION EFFECTIVENESS'
\echo '---'
SELECT
  COUNT(*) as total_observations,
  COUNT(DISTINCT (record_id, record_type, parameter_id, unit_id)) as unique_combinations,
  COUNT(*) - COUNT(DISTINCT (record_id, record_type, parameter_id, unit_id)) as duplicate_keys
FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record');

\echo ''
\echo '6️⃣  SAMPLE CENSUS RECORD'
\echo '---'
SELECT
  id, geoid, year, commodity_code,
  dataset_id, etl_run_id, lineage_group_id,
  created_at, updated_at
FROM usda_census_record
ORDER BY created_at DESC
LIMIT 1;

\echo ''
\echo '7️⃣  SAMPLE SURVEY RECORD'
\echo '---'
SELECT
  id, geoid, year, commodity_code,
  survey_period, reference_month,
  dataset_id, etl_run_id, lineage_group_id,
  created_at, updated_at
FROM usda_survey_record
ORDER BY created_at DESC
LIMIT 1;

\echo ''
\echo '8️⃣  SAMPLE OBSERVATION'
\echo '---'
SELECT
  id, record_id, record_type, parameter_id, unit_id,
  value, value_text, cv_pct, note,
  dataset_id, etl_run_id, lineage_group_id,
  created_at
FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record')
ORDER BY created_at DESC
LIMIT 1;

\echo ''
\echo '========================================'
\echo '✅ Validation Complete'
\echo '========================================'
\echo ''
