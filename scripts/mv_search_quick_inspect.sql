-- Quick inspection for mv_biomass_search
-- DBCode-friendly: plain SQL, compact result sets.

-- 1) General preview of key search fields
SELECT
    id,
    name,
    resource_class,
    resource_subclass,
    primary_product,
    transport_description,
    storage_description,
    transport_notes,
    storage_notes,
    season_from_month,
    season_to_month,
    year_round,
    has_volume_data,
    has_image,
    has_moisture_data,
    has_sugar_data
FROM data_portal.mv_biomass_search
ORDER BY name
LIMIT 12;

-- 2) Only rows that actually have transport or storage text
SELECT
    id,
    name,
    transport_description,
    storage_description
FROM data_portal.mv_biomass_search
WHERE transport_description IS NOT NULL
   OR storage_description IS NOT NULL
ORDER BY name
LIMIT 20;

-- 3) A few likely high-signal biomass rows
SELECT
    id,
    name,
    transport_description,
    storage_description,
    tags,
    resource_class,
    resource_subclass,
    primary_product
FROM data_portal.mv_biomass_search
WHERE lower(name) LIKE '%almond%'
   OR lower(name) LIKE '%grape%'
   OR lower(name) LIKE '%olive%'
ORDER BY name
LIMIT 100;
