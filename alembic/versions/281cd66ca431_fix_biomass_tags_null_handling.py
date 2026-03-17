"""fix biomass tags null handling

Revision ID: 281cd66ca431
Revises: 6a3e85eafe02
Create Date: 2026-03-17 16:06:48.662409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import mv_biomass_search


# revision identifiers, used by Alembic.
revision: str = '281cd66ca431'
down_revision: Union[str, Sequence[str], None] = '6a3e85eafe02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop and recreate mv_biomass_search with updated logic
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search")

    # Generate the CREATE MATERIALIZED VIEW statement from the SQLAlchemy expression
    from sqlalchemy.dialects import postgresql
    engine = op.get_bind().engine
    create_stmt = str(mv_biomass_search.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {create_stmt}")

    # REFRESH MATERIALIZED VIEW CONCURRENTLY requires a UNIQUE index
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_biomass_search_resource_id ON data_portal.mv_biomass_search (id)")


def downgrade() -> None:
    """Downgrade schema."""
    # This is a bit tricky since we'd need the old logic.
    # For now, we just drop it. In a real scenario, we might want to keep the old SQL.
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search")
