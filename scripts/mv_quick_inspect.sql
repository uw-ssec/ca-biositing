-- Quick MV inspection (DBCode-friendly, no psql meta commands)

-- MV 9: mv_biomass_end_uses (few rows)
SELECT resource_id,
       resource_name,
       use_case,
       percentage_low,
       percentage_high,
       trend,
       value_low_usd,
       value_high_usd,
       value_notes
FROM data_portal.mv_biomass_end_uses
ORDER BY resource_name, use_case
LIMIT 12;

-- mv_biomass_search (few rows, transport/storage focus)
SELECT id,
       name,
       transport_description,
       storage_description,
       transport_notes,
       storage_notes
FROM data_portal.mv_biomass_search
ORDER BY name
LIMIT 12;

-- Optional: filter to records where either transport/storage is present
SELECT id,
       name,
       transport_description,
       storage_description
FROM data_portal.mv_biomass_search
WHERE transport_description IS NOT NULL
   OR storage_description IS NOT NULL
ORDER BY name
LIMIT 20;
