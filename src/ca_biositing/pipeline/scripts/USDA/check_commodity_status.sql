-- Check Commodity ETL Status
-- Shows which commodities made it through the ETL vs which are missing

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
