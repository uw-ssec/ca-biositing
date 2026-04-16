-- MV qualitative validation display
-- Purpose: quick operator-facing pass/fail dashboard for MV 9 and search transport/storage coverage.
-- Spec context used here (from material spec sheet):
--   MV 9: mv_biomass_end_uses
--   - Purpose: end use breakdown per resource
--   - Grain: one row per resource x use_case
--   - Frontend-critical fields: use_case, percentage_low/high, trend, value_low/high, value_notes
-- Additional frontend expectation:
--   mv_biomass_search should expose transport_description and storage_description.

SELECT '=== 1) DEPLOYED MV DEFINITIONS (trimmed) ===' AS section;
SELECT schemaname, matviewname, left(definition, 500) AS definition_prefix
FROM pg_matviews
WHERE schemaname = 'data_portal'
  AND matviewname IN ('mv_biomass_end_uses', 'mv_biomass_search')
ORDER BY matviewname;

SELECT '=== 2) COLUMN CONTRACT CHECKS ===' AS section;
WITH required_columns AS (
    SELECT 'mv_biomass_end_uses'::text AS view_name, unnest(ARRAY[
        'resource_id','resource_name','use_case',
        'percentage_low','percentage_high','trend',
        'value_low_usd','value_high_usd','value_notes'
    ]) AS column_name
    UNION ALL
    SELECT 'mv_biomass_search'::text AS view_name, unnest(ARRAY[
        'transport_description','storage_description'
    ]) AS column_name
),
actual_columns AS (
        SELECT c.relname AS view_name,
                     a.attname AS column_name
        FROM pg_class c
        JOIN pg_namespace n
            ON n.oid = c.relnamespace
        JOIN pg_attribute a
            ON a.attrelid = c.oid
        WHERE n.nspname = 'data_portal'
            AND c.relkind = 'm'
            AND c.relname IN ('mv_biomass_end_uses','mv_biomass_search')
            AND a.attnum > 0
            AND NOT a.attisdropped
)
SELECT rc.view_name,
       rc.column_name,
       CASE WHEN ac.column_name IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status
FROM required_columns rc
LEFT JOIN actual_columns ac
  ON ac.view_name = rc.view_name
 AND ac.column_name = rc.column_name
ORDER BY rc.view_name, rc.column_name;

SELECT '=== 3) GRAIN CHECK (MV9 one row per resource x use_case) ===' AS section;
SELECT CASE WHEN EXISTS (
    SELECT 1
    FROM data_portal.mv_biomass_end_uses
    GROUP BY resource_id, use_case
    HAVING COUNT(*) > 1
) THEN 'FAIL' ELSE 'PASS' END AS grain_status,
COALESCE((
    SELECT SUM(dup_count)
    FROM (
        SELECT COUNT(*) - 1 AS dup_count
        FROM data_portal.mv_biomass_end_uses
        GROUP BY resource_id, use_case
        HAVING COUNT(*) > 1
    ) d
), 0) AS duplicate_row_overage;

SELECT '=== 4) POPULATION CHECKS ===' AS section;
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE use_case IS NOT NULL) AS use_case_populated,
    COUNT(*) FILTER (WHERE percentage_low IS NOT NULL OR percentage_high IS NOT NULL) AS percentage_present,
    COUNT(*) FILTER (WHERE value_low_usd IS NOT NULL OR value_high_usd IS NOT NULL) AS value_range_present,
    COUNT(*) FILTER (WHERE trend IS NOT NULL) AS trend_present
FROM data_portal.mv_biomass_end_uses;

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE transport_description IS NOT NULL OR transport_notes IS NOT NULL) AS transport_present,
    COUNT(*) FILTER (WHERE storage_description IS NOT NULL OR storage_notes IS NOT NULL) AS storage_present
FROM data_portal.mv_biomass_search;

SELECT '=== 5) SAMPLE ROWS: MV9 ===' AS section;
SELECT resource_id, resource_name, use_case,
       percentage_low, percentage_high,
       trend, value_low_usd, value_high_usd, value_notes
FROM data_portal.mv_biomass_end_uses
ORDER BY resource_name, use_case
LIMIT 25;

SELECT '=== 6) SAMPLE ROWS: SEARCH TRANSPORT/STORAGE ===' AS section;
SELECT id, name,
       transport_description, storage_description,
       transport_notes, storage_notes
FROM data_portal.mv_biomass_search
ORDER BY name
LIMIT 25;

SELECT '=== 7) QUICK PEEK (TOP 8): mv_biomass_end_uses ===' AS section;
SELECT resource_name,
       use_case,
       percentage_low,
       percentage_high,
       trend,
       value_low_usd,
       value_high_usd,
       value_notes
FROM data_portal.mv_biomass_end_uses
ORDER BY resource_name, use_case
LIMIT 8;

SELECT '=== 8) QUICK PEEK (TOP 8): mv_biomass_search ===' AS section;
SELECT name,
       transport_description,
       storage_description,
       transport_notes,
       storage_notes
FROM data_portal.mv_biomass_search
ORDER BY name
LIMIT 8;
