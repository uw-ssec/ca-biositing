"""Recreate remaining 8 materialized views with raw SQL snapshots.

Consolidates the recreation of all remaining views into a single migration.
Each view SQL was compiled from SQLAlchemy at migration-creation time and
is frozen here as immutable strings for all future replays.

Views included:
- mv_biomass_availability
- mv_biomass_composition
- mv_biomass_county_production
- mv_biomass_sample_stats
- mv_biomass_fermentation
- mv_biomass_gasification
- mv_biomass_pricing
- mv_usda_county_production

Revision ID: 9e8f7a6b5c4f
Revises: 9e8f7a6b5c4e
Create Date: 2026-04-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e8f7a6b5c4f'
down_revision = '9e8f7a6b5c4e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Recreate all 8 remaining views with immutable SQL snapshots."""

    # ========================================================================
    # 1. mv_biomass_availability
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_availability CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_availability AS
        SELECT resource.id AS resource_id, resource.name AS resource_name, min(resource_availability.from_month) AS from_month, max(resource_availability.to_month) AS to_month, bool_or(resource_availability.year_round) AS year_round, avg(resource_availability.residue_factor_dry_tons_acre) AS dry_tons_per_acre, avg(resource_availability.residue_factor_wet_tons_acre) AS wet_tons_per_acre
        FROM resource_availability JOIN resource ON resource_availability.resource_id = resource.id GROUP BY resource.id, resource.name
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_availability_id ON data_portal.mv_biomass_availability (resource_id)
    """)

    # ========================================================================
    # 2. mv_biomass_composition
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_composition AS
        SELECT row_number() OVER (ORDER BY anon_1.resource_id, anon_1.analysis_type, anon_1.parameter_name, anon_1.unit) AS id, anon_1.resource_id, resource.name AS resource_name, anon_1.analysis_type, anon_1.parameter_name, anon_1.unit, avg(anon_1.value) AS avg_value, min(anon_1.value) AS min_value, max(anon_1.value) AS max_value, stddev(anon_1.value) AS std_dev, count(*) AS observation_count
        FROM (SELECT compositional_record.resource_id AS resource_id, 'compositional' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM compositional_record JOIN observation ON lower(observation.record_id) = lower(compositional_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT proximate_record.resource_id AS resource_id, 'proximate' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM proximate_record JOIN observation ON lower(observation.record_id) = lower(proximate_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT ultimate_record.resource_id AS resource_id, 'ultimate' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM ultimate_record JOIN observation ON lower(observation.record_id) = lower(ultimate_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT xrf_record.resource_id AS resource_id, 'xrf' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM xrf_record JOIN observation ON lower(observation.record_id) = lower(xrf_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT icp_record.resource_id AS resource_id, 'icp' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM icp_record JOIN observation ON lower(observation.record_id) = lower(icp_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT calorimetry_record.resource_id AS resource_id, 'calorimetry' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM calorimetry_record JOIN observation ON lower(observation.record_id) = lower(calorimetry_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT xrd_record.resource_id AS resource_id, 'xrd' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM xrd_record JOIN observation ON lower(observation.record_id) = lower(xrd_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id UNION ALL SELECT ftnir_record.resource_id AS resource_id, 'ftnir' AS analysis_type, parameter.name AS parameter_name, observation.value AS value, unit.name AS unit
        FROM ftnir_record JOIN observation ON lower(observation.record_id) = lower(ftnir_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id) AS anon_1 JOIN resource ON anon_1.resource_id = resource.id GROUP BY anon_1.resource_id, resource.name, anon_1.analysis_type, anon_1.parameter_name, anon_1.unit
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)
    """)

    # ========================================================================
    # 3. mv_biomass_county_production
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_county_production CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_county_production AS
        SELECT row_number() OVER (ORDER BY billion_ton2023_record.resource_id, place.geoid, billion_ton2023_record.scenario_name, billion_ton2023_record.price_offered_usd) AS id, billion_ton2023_record.resource_id, resource.name AS resource_name, resource_class.name AS resource_class, place.geoid, place.county_name AS county, place.state_name AS state, billion_ton2023_record.scenario_name AS scenario, billion_ton2023_record.price_offered_usd, billion_ton2023_record.production, unit.name AS production_unit, billion_ton2023_record.production_energy_content AS energy_content, eu.name AS energy_unit, billion_ton2023_record.product_density_dtpersqmi AS density_dt_per_sqmi, billion_ton2023_record.county_square_miles, 2023 AS year
        FROM billion_ton2023_record JOIN resource ON billion_ton2023_record.resource_id = resource.id LEFT OUTER JOIN resource_class ON resource.resource_class_id = resource_class.id LEFT OUTER JOIN unit ON billion_ton2023_record.production_unit_id = unit.id LEFT OUTER JOIN unit AS eu ON billion_ton2023_record.energy_content_unit_id = eu.id JOIN place ON billion_ton2023_record.geoid = place.geoid
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_county_production_id ON data_portal.mv_biomass_county_production (id)
    """)

    # ========================================================================
    # 4. mv_biomass_sample_stats
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_sample_stats CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_sample_stats AS
        SELECT row_number() OVER (ORDER BY observation.record_id) AS sample_id, observation.record_id, observation.record_type, parameter.name AS parameter_name, observation.value, unit.name AS unit, observation.created_at
        FROM observation JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_id ON data_portal.mv_biomass_sample_stats (sample_id)
    """)

    # ========================================================================
    # 5. mv_biomass_fermentation
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_fermentation CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_fermentation AS
        SELECT row_number() OVER (ORDER BY fermentation_record.resource_id, strain.name, pm.name, em.name, parameter.name, unit.name) AS id, fermentation_record.resource_id, resource.name AS resource_name, strain.name AS strain_name, pm.name AS pretreatment_method, em.name AS enzyme_name, parameter.name AS product_name, avg(observation.value) AS avg_value, min(observation.value) AS min_value, max(observation.value) AS max_value, stddev(observation.value) AS std_dev, count(*) AS observation_count, unit.name AS unit
        FROM fermentation_record JOIN resource ON fermentation_record.resource_id = resource.id LEFT OUTER JOIN strain ON fermentation_record.strain_id = strain.id LEFT OUTER JOIN method AS pm ON fermentation_record.pretreatment_method_id = pm.id LEFT OUTER JOIN method AS em ON fermentation_record.eh_method_id = em.id JOIN observation ON lower(observation.record_id) = lower(fermentation_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id GROUP BY fermentation_record.resource_id, resource.name, strain.name, pm.name, em.name, parameter.name, unit.name
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)
    """)

    # ========================================================================
    # 6. mv_biomass_gasification
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_gasification CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_gasification AS
        SELECT row_number() OVER (ORDER BY gasification_record.resource_id, decon_vessel.name, parameter.name, unit.name) AS id, gasification_record.resource_id, resource.name AS resource_name, decon_vessel.name AS reactor_type, parameter.name AS parameter_name, avg(observation.value) AS avg_value, min(observation.value) AS min_value, max(observation.value) AS max_value, stddev(observation.value) AS std_dev, count(*) AS observation_count, unit.name AS unit
        FROM gasification_record JOIN resource ON gasification_record.resource_id = resource.id LEFT OUTER JOIN decon_vessel ON gasification_record.reactor_type_id = decon_vessel.id JOIN observation ON lower(observation.record_id) = lower(gasification_record.record_id) JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id GROUP BY gasification_record.resource_id, resource.name, decon_vessel.name, parameter.name, unit.name
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)
    """)

    # ========================================================================
    # 7. mv_biomass_pricing
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_pricing CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_biomass_pricing AS
        SELECT row_number() OVER (ORDER BY usda_market_record.id) AS id, usda_commodity.name AS commodity_name, place.geoid, place.county_name AS county, place.state_name AS state, usda_market_record.report_date, usda_market_record.market_type_category, usda_market_record.sale_type, anon_1.price_min, anon_1.price_max, anon_1.price_avg, anon_1.price_unit
        FROM usda_market_record JOIN usda_market_report ON usda_market_record.report_id = usda_market_report.id JOIN usda_commodity ON usda_market_record.commodity_id = usda_commodity.id LEFT OUTER JOIN location_address ON usda_market_report.office_city_id = location_address.id LEFT OUTER JOIN place ON location_address.geography_id = place.geoid JOIN (SELECT observation.record_id AS record_id, avg(observation.value) AS price_avg, min(observation.value) AS price_min, max(observation.value) AS price_max, unit.name AS price_unit
        FROM observation JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id
        WHERE observation.record_type = 'usda_market_record' AND lower(parameter.name) = 'price received' GROUP BY observation.record_id, unit.name) AS anon_1 ON CAST(usda_market_record.id AS VARCHAR) = anon_1.record_id
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_biomass_pricing_id ON data_portal.mv_biomass_pricing (id)
    """)

    # ========================================================================
    # 8. mv_usda_county_production
    # ========================================================================
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_usda_county_production AS
        SELECT row_number() OVER (ORDER BY resource.id, place.geoid, usda_census_record.year) AS id, resource.id AS resource_id, resource.name AS resource_name, primary_ag_product.name AS primary_ag_product, place.geoid, place.county_name AS county, place.state_name AS state, usda_census_record.year AS dataset_year, avg(anon_1.primary_product_volume) AS primary_product_volume, max(anon_1.volume_unit) AS volume_unit, avg(anon_1.production_acres) AS production_acres, NULL AS known_biomass_volume, avg(anon_1.production_acres) * coalesce(max(CASE WHEN (anon_2.geoid = place.geoid) THEN anon_2.residue_factor_dry_tons_acre END), max(CASE WHEN (anon_2.geoid = '06000') THEN anon_2.residue_factor_dry_tons_acre END)) AS calculated_estimate_volume, 'dry_tons_acre' AS biomass_unit
        FROM usda_census_record JOIN resource_usda_commodity_map ON usda_census_record.commodity_code = resource_usda_commodity_map.usda_commodity_id JOIN resource ON resource_usda_commodity_map.resource_id = resource.id JOIN primary_ag_product ON resource.primary_ag_product_id = primary_ag_product.id JOIN place ON usda_census_record.geoid = place.geoid JOIN (SELECT observation.record_id AS record_id, avg(CASE WHEN (lower(parameter.name) = 'production') THEN observation.value END) AS primary_product_volume, max(CASE WHEN (lower(parameter.name) = 'production') THEN unit.name END) AS volume_unit, avg(CASE WHEN (lower(parameter.name) IN ('area bearing', 'area harvested', 'area in production') AND lower(unit.name) = 'acres') THEN observation.value END) AS production_acres
        FROM observation JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id
        WHERE observation.record_type = 'usda_census_record' GROUP BY observation.record_id) AS anon_1 ON CAST(usda_census_record.id AS VARCHAR) = anon_1.record_id LEFT OUTER JOIN (SELECT resource_availability.resource_id AS resource_id, resource_availability.geoid AS geoid, resource_availability.residue_factor_dry_tons_acre AS residue_factor_dry_tons_acre
        FROM resource_availability) AS anon_2 ON resource.id = anon_2.resource_id
        WHERE usda_census_record.year = 2022 GROUP BY resource.id, resource.name, primary_ag_product.name, place.geoid, place.county_name, place.state_name, usda_census_record.year
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)
    """)

    # Grant schema access to readonly role (applies to all views)
    op.execute("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly")
    op.execute("GRANT SELECT ON ALL MATERIALIZED VIEWS IN SCHEMA data_portal TO biocirv_readonly")


def downgrade() -> None:
    """Drop all recreated views."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_availability CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_county_production CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_sample_stats CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_fermentation CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_gasification CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_pricing CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")
