"""Fix analysis_data_view joins and resource mapping

Revision ID: fix_analysis_view_joins
Revises: 3b255400a04e
Create Date: 2026-02-27 00:07:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import dialect as pg_dialect

# Import materialized view definitions
from ca_biositing.datamodels.views import (
    VIEW_SCHEMA,
    ANALYSIS_DATA_VIEW,
    ANALYSIS_AVERAGE_VIEW_SQL
)

# revision identifiers, used by Alembic.
revision: str = 'fix_analysis_view_joins'
down_revision: Union[str, Sequence[str], None] = '3b255400a04e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop dependent view first
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.analysis_average_view CASCADE")
    # Drop and recreate analysis_data_view
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.analysis_data_view CASCADE")

    compiled = ANALYSIS_DATA_VIEW.compile(
        dialect=pg_dialect(), compile_kwargs={"literal_binds": True}
    )
    op.execute(
        f"CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.analysis_data_view AS {compiled}"
    )

    # Recreate analysis_average_view
    op.execute(
        f"CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.analysis_average_view AS "
        f"{ANALYSIS_AVERAGE_VIEW_SQL}"
    )


def downgrade() -> None:
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.analysis_average_view CASCADE")
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.analysis_data_view CASCADE")
