"""Refine mv_usda_county_production logic

Revision ID: 9f428a5703f7
Revises: 386622baae98
Create Date: 2026-03-24 10:05:35.771448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f428a5703f7'
down_revision: Union[str, Sequence[str], None] = '386622baae98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from ca_biositing.datamodels.data_portal_views import mv_usda_county_production


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing view
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")

    # Create revised view
    compiled = mv_usda_county_production.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_usda_county_production AS {str(compiled)}")

    # Recreate indexes
    op.execute("CREATE UNIQUE INDEX idx_mv_usda_county_production_id ON data_portal.mv_usda_county_production (id)")
    op.execute("CREATE INDEX idx_mv_usda_county_production_resource_id ON data_portal.mv_usda_county_production (resource_id)")
    op.execute("CREATE INDEX idx_mv_usda_county_production_geoid ON data_portal.mv_usda_county_production (geoid)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_usda_county_production CASCADE")
