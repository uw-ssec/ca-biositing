"""add_mv_usda_county_production_and_update_existing_views

Revision ID: 6a3e85eafe02
Revises: 7d1e5a1f0c38
Create Date: 2026-03-16 17:04:07.564147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import (
    mv_biomass_gasification,
    mv_biomass_pricing,
    mv_usda_county_production
)


# revision identifiers, used by Alembic.
revision: str = '6a3e85eafe02'
down_revision: Union[str, Sequence[str], None] = '7d1e5a1f0c38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop views that are being updated or replaced
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_gasification CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_pricing CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")

    def create_mv(name, stmt):
        # Use literal_binds=True to inline parameters
        compiled = stmt.compile(
            dialect=sa.dialects.postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
        sql = str(compiled)
        op.execute(f"CREATE MATERIALIZED VIEW data_portal.{name} AS {sql}")

    # Create/Recreate views
    create_mv("mv_biomass_gasification", mv_biomass_gasification)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)")

    create_mv("mv_biomass_pricing", mv_biomass_pricing)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_pricing_id ON data_portal.mv_biomass_pricing (id)")

    create_mv("mv_usda_county_production", mv_usda_county_production)
    op.execute("CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)")
    op.execute("CREATE INDEX idx_mv_usda_county_production_resource_id ON data_portal.mv_usda_county_production (resource_id)")
    op.execute("CREATE INDEX idx_mv_usda_county_production_geoid ON data_portal.mv_usda_county_production (geoid)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_pricing CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_gasification CASCADE")
