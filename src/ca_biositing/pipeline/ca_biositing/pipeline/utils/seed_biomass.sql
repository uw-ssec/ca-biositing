-- This script inserts 10 sample rows into the biomass table.
-- Note: This assumes that valid records exist in the primary_product, taxonomy, and biomass_type tables
-- for the foreign key IDs used below.

INSERT INTO biomass (biomass_name, primary_product_id, taxonomy_id, biomass_type_id, biomass_notes) VALUES
('Corn Stover', 1, 101, 1, 'Lignocellulosic biomass from corn stalks and leaves.'),
('Switchgrass', 2, 102, 1, 'Perennial grass used as a dedicated energy crop.'),
('Pine Wood Chips', 3, 103, 2, 'Woody biomass from pine trees, chipped for processing.'),
('Algae Culture', 4, 104, 3, 'Aquatic biomass grown for biofuel production.'),
('Municipal Solid Waste (MSW)', 5, 105, 4, 'Organic fraction of household waste.'),
('Food Waste', 6, 106, 4, 'Post-consumer food scraps from restaurants.'),
('Manure Slurry', 7, 107, 5, 'Animal waste from dairy farms, used in anaerobic digestion.'),
('Miscanthus Giganteus', 2, 108, 1, 'High-yield sterile hybrid grass for bioenergy.'),
('Willow Coppice', 3, 109, 2, 'Short-rotation coppice willow for biomass energy.'),
('Sugarcane Bagasse', 1, 110, 1, 'Fibrous residue left after sugarcane crushing.');
