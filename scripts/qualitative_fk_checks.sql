-- Human-readable observation view for end-use qualitative rows.
SELECT
    o.id AS observation_id,
    o.record_id AS end_use_record_id,
    r.id AS resource_id,
    r.name AS resource_name,
    uc.id AS use_case_id,
    uc.name AS use_case_name,
    p.id AS parameter_id,
    p.name AS parameter_name,
    u.id AS unit_id,
    u.name AS unit_name,
    o.value,
    o.note,
    CASE
        WHEN p.name = 'resource_use_trend' THEN
            CASE
                WHEN lower(trim(coalesce(o.note, ''))) IN ('up', 'increase', 'increasing', 'rising') THEN 1
                WHEN lower(trim(coalesce(o.note, ''))) IN ('down', 'decrease', 'decreasing', 'falling') THEN -1
                WHEN lower(trim(coalesce(o.note, ''))) IN ('steady', 'stable', 'flat', 'no change') THEN 0
                ELSE NULL
            END
        ELSE NULL
    END AS trend_code
FROM observation o
JOIN resource_end_use_record eur
    ON eur.id::text = o.record_id
   AND o.record_type = 'resource_end_use_record'
LEFT JOIN resource r ON r.id = eur.resource_id
LEFT JOIN use_case uc ON uc.id = eur.use_case_id
LEFT JOIN parameter p ON p.id = o.parameter_id
LEFT JOIN unit u ON u.id = o.unit_id
ORDER BY o.id;


-- Same query, filtered to a specific parameter id (replace 2 as needed).
SELECT
    o.id AS observation_id,
    o.record_id AS end_use_record_id,
    r.name AS resource_name,
    uc.name AS use_case_name,
    p.name AS parameter_name,
    o.value,
    o.note
FROM observation o
JOIN resource_end_use_record eur
    ON eur.id::text = o.record_id
   AND o.record_type = 'resource_end_use_record'
LEFT JOIN resource r ON r.id = eur.resource_id
LEFT JOIN use_case uc ON uc.id = eur.use_case_id
LEFT JOIN parameter p ON p.id = o.parameter_id
WHERE o.parameter_id = 2
ORDER BY o.id;


-- Almond hull/shell duplicate audit in storage + transport record tables.
SELECT
    t.table_name,
    t.record_id,
    t.resource_id,
    r.name AS resource_name,
    t.description
FROM (
    SELECT
        'resource_storage_record'::text AS table_name,
        rsr.id AS record_id,
        rsr.resource_id,
        rsr.storage_description AS description
    FROM resource_storage_record rsr

    UNION ALL

    SELECT
        'resource_transport_record'::text AS table_name,
        rtr.id AS record_id,
        rtr.resource_id,
        rtr.transport_description AS description
    FROM resource_transport_record rtr
) t
LEFT JOIN resource r ON r.id = t.resource_id
WHERE lower(coalesce(r.name, '')) LIKE '%almond hull%'
   OR lower(coalesce(r.name, '')) LIKE '%almond shell%'
   OR t.resource_id IN (118, 119)
ORDER BY t.table_name, t.record_id;


-- Use-case rows and whether they are referenced by end-use records.
SELECT
    uc.id,
    uc.name,
    COUNT(eur.id) AS end_use_reference_count
FROM use_case uc
LEFT JOIN resource_end_use_record eur ON eur.use_case_id = uc.id
GROUP BY uc.id, uc.name
ORDER BY end_use_reference_count DESC, uc.name;
