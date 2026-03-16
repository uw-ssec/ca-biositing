"""Update data portal views logic

Revision ID: 5f14811d264f
Revises: 23a53daf6d9f
Create Date: 2026-03-16 11:24:06.273089

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import (
    mv_biomass_search,
    mv_biomass_composition,
    mv_biomass_county_production,
    mv_biomass_availability,
    mv_biomass_sample_stats,
    mv_biomass_fermentation,
    mv_biomass_gasification
)

# revision identifiers, used by Alembic.
revision: str = '5f14811d264f'
down_revision: Union[str, Sequence[str], None] = '23a53daf6d9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing views to recreate with new logic
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_county_production CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_availability CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_sample_stats CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_fermentation CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_gasification CASCADE")

    def create_mv(name, stmt):
        compiled = stmt.compile(dialect=sa.dialects.postgresql.dialect(), compile_kwargs={"literal_binds": True})
        op.execute(f"CREATE MATERIALIZED VIEW data_portal.{name} AS {compiled}")

    # Recreate views with updated logic
    create_mv("mv_biomass_search", mv_biomass_search)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)")
    op.execute("CREATE INDEX idx_mv_biomass_search_name_trgm ON data_portal.mv_biomass_search USING gin (name gin_trgm_ops)")
    op.execute("CREATE INDEX idx_mv_biomass_search_vector ON data_portal.mv_biomass_search USING gin (search_vector)")

    create_mv("mv_biomass_composition", mv_biomass_composition)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)")

    create_mv("mv_biomass_county_production", mv_biomass_county_production)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_county_production_id ON data_portal.mv_biomass_county_production (id)")

    create_mv("mv_biomass_availability", mv_biomass_availability)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_availability_resource_id ON data_portal.mv_biomass_availability (resource_id)")

    create_mv("mv_biomass_sample_stats", mv_biomass_sample_stats)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_resource_id ON data_portal.mv_biomass_sample_stats (resource_id)")

    create_mv("mv_biomass_fermentation", mv_biomass_fermentation)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)")

    create_mv("mv_biomass_gasification", mv_biomass_gasification)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_gasification_id ON data_portal.mv_biomass_gasification (id)")

def downgrade() -> None:
    """Downgrade schema (not implemented as it involves reverting complex logic)."""
    pass
