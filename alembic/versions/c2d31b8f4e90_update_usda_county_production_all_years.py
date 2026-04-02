"""Update USDA county production view to include all years

Revision ID: c2d31b8f4e90
Revises: 9f4c2d8a7b11
Create Date: 2026-04-02 15:05:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from ca_biositing.datamodels.data_portal_views import mv_usda_county_production

# revision identifiers, used by Alembic.
revision: str = "c2d31b8f4e90"
down_revision: Union[str, Sequence[str], None] = "9f4c2d8a7b11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DATA_PORTAL_SCHEMA = "data_portal"


def _create_mv(name: str, stmt) -> None:
    compiled = stmt.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True},
    )
    op.execute(f"CREATE MATERIALIZED VIEW {DATA_PORTAL_SCHEMA}.{name} AS {compiled}")


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        f"DROP MATERIALIZED VIEW IF EXISTS {DATA_PORTAL_SCHEMA}.mv_usda_county_production CASCADE"
    )
    _create_mv("mv_usda_county_production", mv_usda_county_production)
    op.execute(
        f"CREATE UNIQUE INDEX idx_mv_usda_county_production_id "
        f"ON {DATA_PORTAL_SCHEMA}.mv_usda_county_production (id)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        f"DROP MATERIALIZED VIEW IF EXISTS {DATA_PORTAL_SCHEMA}.mv_usda_county_production CASCADE"
    )
