-- Debug Missing Commodities
-- Shows which commodities are missing and why

-- Commodities with no data
SELECT
    uc.api_name,
    uc.name,
    uc.usda_code,
    'NO_DATA' as issue
FROM usda_commodity uc
WHERE NOT EXISTS (
    SELECT 1 FROM usda_census_record ucr
    WHERE ucr.commodity_code = uc.id
)
ORDER BY uc.api_name;
