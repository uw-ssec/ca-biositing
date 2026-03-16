"""Integrate pretreatment into data portal views and fix fermentation join

Revision ID: 3a9adc1f9228
Revises: 6a7d2cde4f41
Create Date: 2026-03-16 12:52:16.332730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import (
    mv_biomass_search,
    mv_biomass_composition,
    mv_biomass_sample_stats,
    mv_biomass_fermentation
)


# revision identifiers, used by Alembic.
revision: str = '3a9adc1f9228'
down_revision: Union[str, Sequence[str], None] = '6a7d2cde4f41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop views that are being updated
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_composition CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_sample_stats CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_fermentation CASCADE")

    def create_mv(name, stmt):
        # Use literal_binds=True to inline parameters
        compiled = stmt.compile(
            dialect=sa.dialects.postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
        # Handle REGCONFIG specifically since literal_binds fails for it
        sql = str(compiled).replace("CAST('english' AS TEXT)", "'english'")
        op.execute(f"CREATE MATERIALIZED VIEW data_portal.{name} AS {sql}")

    # Recreate views with updated logic
    create_mv("mv_biomass_search", mv_biomass_search)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)")
    op.execute("CREATE INDEX idx_mv_biomass_search_name_trgm ON data_portal.mv_biomass_search USING gin (name gin_trgm_ops)")
    op.execute("CREATE INDEX idx_mv_biomass_search_vector ON data_portal.mv_biomass_search USING gin (search_vector)")

    create_mv("mv_biomass_composition", mv_biomass_composition)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_composition_id ON data_portal.mv_biomass_composition (id)")

    create_mv("mv_biomass_sample_stats", mv_biomass_sample_stats)
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_sample_stats_resource_id ON data_portal.mv_biomass_sample_stats (resource_id)")

    create_mv("mv_biomass_fermentation", mv_biomass_fermentation)
    # Ensure ID column is present if using row_number
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_fermentation_id ON data_portal.mv_biomass_fermentation (id)")


def downgrade() -> None:
    """Downgrade schema."""
    pass
