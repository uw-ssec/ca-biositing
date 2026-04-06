"""drop_incumbent_data_portal_views

Drop the old monolithic data_portal_views before recreating with new modular approach.

Revision ID: 9e8f7a6b5c4d
Revises: 60b08397200f
Create Date: 2026-04-04 02:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e8f7a6b5c4d'
down_revision: Union[str, Sequence[str], None] = '60b08397200f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Drop all incumbent materialized views from the old monolithic data_portal_views.py file.

    This clears the database state before recreating views using the new modular approach.
    Views will be recreated one by one in subsequent migrations with immutable SQL snapshots.

    Dropped views:
    - mv_biomass_search
    - mv_biomass_composition
    - mv_biomass_county_production
    - mv_biomass_availability
    - mv_biomass_sample_stats
    - mv_biomass_fermentation
    - mv_biomass_gasification
    - mv_biomass_pricing
    - mv_usda_county_production
    """
    # Drop all dependent indexes first, then views (CASCADE handles this)
    views_to_drop = [
        'mv_biomass_search',
        'mv_biomass_composition',
        'mv_biomass_county_production',
        'mv_biomass_availability',
        'mv_biomass_sample_stats',
        'mv_biomass_fermentation',
        'mv_biomass_gasification',
        'mv_biomass_pricing',
        'mv_usda_county_production'
    ]

    for view in views_to_drop:
        op.execute(f"DROP MATERIALIZED VIEW IF EXISTS data_portal.{view} CASCADE")

    # Grant schema access to biocirv_readonly user
    # This ensures the user can access all future views in the data_portal schema
    op.execute("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly")
    op.execute("GRANT SELECT ON ALL TABLES IN SCHEMA data_portal TO biocirv_readonly")
    op.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA data_portal GRANT SELECT ON TABLES TO biocirv_readonly")


def downgrade() -> None:
    """Downgrade: revoke permissions (views would need to be manually recreated)."""
    op.execute("REVOKE SELECT ON ALL TABLES IN SCHEMA data_portal FROM biocirv_readonly")
    op.execute("REVOKE USAGE ON SCHEMA data_portal FROM biocirv_readonly")
