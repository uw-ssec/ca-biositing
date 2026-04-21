"""Phase 3: Add mv_volume_estimation materialized view

Revision ID: a8b9c7d6e5f4
Revises: a721de1a5850
Create Date: 2026-04-20 20:09:00.000000

This migration creates the new mv_volume_estimation materialized view that combines
production-based and census-based volume estimation for biomass resources.

Path A (Production-based): Uses county_ag_report_record × residue_factors for most
agricultural residues.

Path B (Census-based): Uses USDA census bearing_acres × prune_trim_yield for
orchard crops.

The view uses raw SQL snapshots (immutable) to ensure reliable migrations and
teardown→rebuild scenarios.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8b9c7d6e5f4'
down_revision = 'a721de1a5850'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create mv_volume_estimation with immutable SQL snapshot."""

    # Drop the view if it exists (from broken migrations)
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_volume_estimation CASCADE")

    # Create the view with raw SQL snapshot
    # This SQL was compiled from SQLAlchemy at migration-creation time
    # and is frozen here for all future replays (immutable, not runtime-evaluated)
    # Path A: Production-based volumes (county_ag_report_record × residue_factors)
    # Path B: Census-based volumes (usda_census_record × prune_trim_yield)
    op.execute("""
        CREATE MATERIALIZED VIEW data_portal.mv_volume_estimation AS
        SELECT row_number() OVER (ORDER BY anon_1.resource_id, anon_1.geoid, anon_1.dataset_year, anon_1.volume_source) AS id, anon_1.resource_id, anon_1.resource_name, anon_1.geoid, anon_1.county, anon_1.state, anon_1.dataset_year, anon_1.primary_product_volume AS production_volume, anon_1.volume_unit AS production_unit, anon_1.factor_min, anon_1.factor_mid, anon_1.factor_max, anon_1.estimated_residue_volume_min, anon_1.estimated_residue_volume_mid, anon_1.estimated_residue_volume_max, anon_1.volume_source, anon_1.biomass_unit
        FROM (SELECT resource.id AS resource_id, resource.name AS resource_name, county_ag_report_record.geoid AS geoid, place.county_name AS county, place.state_name AS state, county_ag_report_record.data_year AS dataset_year, county_ag_report_record.record_id AS record_id, avg(observation.value) AS primary_product_volume, max(unit.name) AS volume_unit, residue_factor.factor_min AS factor_min, residue_factor.factor_mid AS factor_mid, residue_factor.factor_max AS factor_max, avg(observation.value) * residue_factor.factor_min AS estimated_residue_volume_min, avg(observation.value) * residue_factor.factor_mid AS estimated_residue_volume_mid, avg(observation.value) * residue_factor.factor_max AS estimated_residue_volume_max, 'production_based' AS volume_source, 'dry_tons' AS biomass_unit
        FROM county_ag_report_record
        JOIN resource ON county_ag_report_record.primary_ag_product_id = resource.primary_ag_product_id
        JOIN residue_factor ON residue_factor.resource_id = resource.id
        JOIN place ON county_ag_report_record.geoid = place.geoid
        LEFT OUTER JOIN observation ON observation.record_id = county_ag_report_record.record_id AND observation.record_type = 'county_ag_report_record'
        LEFT OUTER JOIN unit ON observation.unit_id = unit.id
        WHERE residue_factor.factor_type = 'weight' AND county_ag_report_record.data_year >= 2017 GROUP BY resource.id, resource.name, county_ag_report_record.geoid, place.county_name, place.state_name, county_ag_report_record.data_year, county_ag_report_record.record_id, residue_factor.factor_min, residue_factor.factor_mid, residue_factor.factor_max) AS anon_1 UNION ALL SELECT row_number() OVER (ORDER BY anon_2.resource_id, anon_2.geoid, anon_2.dataset_year, anon_2.volume_source) AS id, anon_2.resource_id, anon_2.resource_name, anon_2.geoid, anon_2.county, anon_2.state, anon_2.dataset_year, anon_2.bearing_acres AS production_volume, anon_2.volume_unit AS production_unit, NULL AS factor_min, NULL AS factor_mid, NULL AS factor_max, anon_2.estimated_residue_volume_min, anon_2.estimated_residue_volume_mid, anon_2.estimated_residue_volume_max, anon_2.volume_source, anon_2.biomass_unit
        FROM (SELECT resource.id AS resource_id, resource.name AS resource_name, usda_census_record.geoid AS geoid, place.county_name AS county, place.state_name AS state, usda_census_record.year AS dataset_year, usda_census_record.id AS record_id, avg(observation.value) AS bearing_acres, 'acres' AS volume_unit, residue_factor.prune_trim_yield AS prune_trim_yield, residue_factor.prune_trim_yield_unit_id AS prune_trim_yield_unit_id, max(unit.name) AS yield_unit, avg(observation.value) * residue_factor.prune_trim_yield AS estimated_residue_volume_min, avg(observation.value) * residue_factor.prune_trim_yield AS estimated_residue_volume_mid, avg(observation.value) * residue_factor.prune_trim_yield AS estimated_residue_volume_max, 'census_bearing_acres' AS volume_source, 'dry_tons' AS biomass_unit
        FROM usda_census_record
        JOIN usda_commodity ON usda_census_record.commodity_code = usda_commodity.id
        JOIN resource_usda_commodity_map ON resource_usda_commodity_map.usda_commodity_id = usda_commodity.id
        JOIN resource ON resource.id = resource_usda_commodity_map.resource_id
        JOIN residue_factor ON residue_factor.resource_id = resource.id
        JOIN place ON usda_census_record.geoid = place.geoid
        LEFT OUTER JOIN observation ON observation.record_id = CAST(usda_census_record.id AS VARCHAR) AND observation.record_type = 'usda_census_record'
        LEFT OUTER JOIN unit ON residue_factor.prune_trim_yield_unit_id = unit.id
        WHERE residue_factor.prune_trim_yield IS NOT NULL AND usda_census_record.year >= 2017 GROUP BY resource.id, resource.name, usda_census_record.geoid, place.county_name, place.state_name, usda_census_record.year, usda_census_record.id, residue_factor.prune_trim_yield, residue_factor.prune_trim_yield_unit_id) AS anon_2
    """)

    # Recreate the unique index for performance
    # This index enables efficient lookups by id and supports the materialized view
    op.execute("""
        CREATE UNIQUE INDEX idx_mv_volume_estimation_id
        ON data_portal.mv_volume_estimation (id)
    """)

    # Grant select permissions to readonly user
    op.execute("GRANT SELECT ON data_portal.mv_volume_estimation TO biocirv_readonly")


def downgrade() -> None:
    """Downgrade: drop the view."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_volume_estimation CASCADE")
