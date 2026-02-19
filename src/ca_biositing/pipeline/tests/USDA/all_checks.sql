-- Combined USDA ETL Validation Script
-- Copy-paste this entire script into your psql session

-- 1. Overall record counts
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

-- 2. Commodity success status
SELECT
    uc.api_name,
    uc.name,
    CASE
        WHEN ucr.commodity_code IS NOT NULL THEN 'SUCCESS'
        ELSE 'MISSING'
    END as status,
    COUNT(ucr.id) as record_count
FROM usda_commodity uc
LEFT JOIN usda_census_record ucr ON uc.id = ucr.commodity_code
GROUP BY uc.id, uc.api_name, uc.name, ucr.commodity_code
ORDER BY status DESC, uc.api_name;

-- 3. Missing commodities
SELECT
    uc.api_name,
    uc.name,
    'NO_DATA' as issue
FROM usda_commodity uc
WHERE NOT EXISTS (
    SELECT 1 FROM usda_census_record ucr
    WHERE ucr.commodity_code = uc.id
)
ORDER BY uc.api_name;
