-- Bootstrap USDA commodity mappings
-- This maps USDA commodity codes to your system's commodities

-- First, ensure commodities exist
INSERT INTO commodity (name, description) VALUES
    ('CORN', 'Corn grain'),
    ('WHEAT', 'Wheat'),
    ('SOYBEANS', 'Soybean'),
    ('COTTON', 'Cotton'),
    ('RICE', 'Rice')
ON CONFLICT (name) DO NOTHING;

-- Then map them to USDA codes
-- USDA uses numeric commodity codes (e.g., 41, 81, 111, etc.)
INSERT INTO resource_usda_commodity_map (commodity_id, usda_commodity_code, usda_commodity_name, notes)
SELECT
    c.id,
    usda_code,
    usda_name,
    'Bootstrap mapping'
FROM (
    VALUES
        (41, 'CORN'),      -- Corn
        (81, 'WHEAT'),     -- Wheat
        (111, 'SOYBEANS'), -- Soybeans
        (131, 'COTTON'),   -- Cotton
        (151, 'RICE')      -- Rice
) AS mapping(usda_code, commodity_name)
JOIN commodity c ON c.name = mapping.commodity_name
WHERE NOT EXISTS (
    SELECT 1 FROM resource_usda_commodity_map rcm
    WHERE rcm.usda_commodity_code = mapping.usda_code
)
ON CONFLICT (usda_commodity_code) DO NOTHING;
