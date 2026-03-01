-- Quick ETL Summary Check
-- Shows high-level record counts across all tables
-- Usage: Copy-paste this entire script into psql

-- Overall record counts
SELECT 'Dataset records' as table_name, COUNT(*) as count FROM dataset
UNION ALL
SELECT 'USDA census records', COUNT(*) FROM usda_census_record
UNION ALL
SELECT 'USDA survey records', COUNT(*) FROM usda_survey_record
UNION ALL
SELECT 'Total observations', COUNT(*) FROM observation
UNION ALL
SELECT 'USDA observations', COUNT(*) FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record')
ORDER BY table_name;
