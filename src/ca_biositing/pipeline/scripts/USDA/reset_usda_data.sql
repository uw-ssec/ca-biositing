-- Reset USDA Data (Safe - keeps other data)
-- Use this between test runs to clean USDA records only

-- Step 1: Delete USDA observations
DELETE FROM observation
WHERE record_type IN ('usda_census_record', 'usda_survey_record');

-- Step 2: Truncate USDA record tables (keeps sequences intact for reference)
TRUNCATE TABLE usda_census_record CASCADE;
TRUNCATE TABLE usda_survey_record CASCADE;

-- Step 3: Delete USDA datasets
DELETE FROM dataset WHERE name LIKE 'USDA_%';

-- Step 4: Optionally delete USDA DataSource (leave if you may use again)
-- DELETE FROM data_source WHERE name = 'USDA NASS API';

-- Step 5: Reset sequences so IDs start from 1
ALTER SEQUENCE usda_census_record_id_seq RESTART WITH 1;
ALTER SEQUENCE usda_survey_record_id_seq RESTART WITH 1;

-- Verify reset
SELECT 'usda_census_record' as table_name, COUNT(*) as row_count FROM usda_census_record
UNION ALL
SELECT 'usda_survey_record', COUNT(*) FROM usda_survey_record
UNION ALL
SELECT 'observation (USDA)', COUNT(*) FROM observation WHERE record_type IN ('usda_census_record', 'usda_survey_record')
UNION ALL
SELECT 'dataset (USDA)', COUNT(*) FROM dataset WHERE name LIKE 'USDA_%';
