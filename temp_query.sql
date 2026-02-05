SELECT DISTINCT uc.name
FROM usda_commodity uc
JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
WHERE rcm.match_tier != 'UNMAPPED'
ORDER BY uc.name;
