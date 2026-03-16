"""Phase 2 Tags: Add percentile-based array column to mv_biomass_search

Revision ID: 7d1e5a1f0c38
Revises: 3a9adc1f9228
Create Date: 2026-03-16 13:12:56.504599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import mv_biomass_search


# revision identifiers, used by Alembic.
revision: str = '7d1e5a1f0c38'
down_revision: Union[str, Sequence[str], None] = '3a9adc1f9228'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop views that are being updated
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")

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


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
