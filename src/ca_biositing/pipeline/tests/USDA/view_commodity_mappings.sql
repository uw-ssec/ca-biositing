-- View Commodity Mappings
-- Human-readable display of resource to USDA commodity mappings
-- Usage: psql -U biocirv_user -d biocirv_db -f scripts/view_commodity_mappings.sql

\echo '\n=== USDA Commodity Mappings Summary ==='
\echo 'Resource Name → USDA Commodity (Match Type)'
\echo '============================================'

SELECT
    r.name as resource_name,
    uc.name as commodity_name,
    uc.usda_code as commodity_code,
    rcm.match_tier,
    CASE
        WHEN rcm.note LIKE '%similarity: %' THEN
            SUBSTRING(rcm.note FROM 'similarity: ([0-9]+\.[0-9]+%)')
        ELSE 'N/A'
    END as similarity,
    rcm.updated_at::date as last_updated
FROM resource_usda_commodity_map rcm
JOIN resource r ON rcm.resource_id = r.id
LEFT JOIN usda_commodity uc ON rcm.usda_commodity_id = uc.id
WHERE rcm.match_tier != 'UNMAPPED'
ORDER BY rcm.match_tier, r.name;

\echo '\n=== Summary by Match Type ==='
SELECT
    match_tier,
    COUNT(*) as count
FROM resource_usda_commodity_map
WHERE match_tier != 'UNMAPPED'
GROUP BY match_tier
ORDER BY match_tier;

\echo '\n=== Unmapped Resources ==='
SELECT
    r.name as unmapped_resource
FROM resource_usda_commodity_map rcm
JOIN resource r ON rcm.resource_id = r.id
WHERE rcm.match_tier = 'UNMAPPED'
ORDER BY r.name;
