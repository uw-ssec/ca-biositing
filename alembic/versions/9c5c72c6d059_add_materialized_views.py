"""add_materialized_views

Revision ID: 9c5c72c6d059
Revises: f5c8c031aef9
Create Date: 2026-02-11 21:25:31.229772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import dialect as pg_dialect

# Import materialized view definitions
from ca_biositing.datamodels.views import (
    VIEW_SCHEMA,
    VIEW_DEFINITIONS,
    ANALYSIS_AVERAGE_VIEW_SQL,
    SPATIAL_VIEW_INDEXES,
)

# revision identifiers, used by Alembic.
revision: str = '9c5c72c6d059'
down_revision: Union[str, Sequence[str], None] = 'f5c8c031aef9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create materialized views from Core select() expressions.
    # Skip USDA views here — they reference api_name which is added in a085cd4a462e.
    # The USDA views are created below with original 'name' column and updated to
    # use 'api_name' in migration b6aa2fc6cd42.
    for view_name, view_query in VIEW_DEFINITIONS:
        if view_name in ("usda_census_view", "usda_survey_view"):
            continue
        compiled = view_query.compile(
            dialect=pg_dialect(), compile_kwargs={"literal_binds": True}
        )
        op.execute(
            f"CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.{view_name} AS {compiled}"
        )

    # Create USDA views with original 'name' column (api_name added later in a085cd4a462e)
    op.execute(
        f"""
        CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.usda_census_view AS
        SELECT
          obs.id,
          uc.name AS usda_crop,
          p.geoid,
          param.name AS parameter,
          obs.value,
          u.name AS unit,
          dt.name AS dimension,
          obs.dimension_value,
          du.name AS dimension_unit
        FROM public.observation obs
        JOIN public.usda_census_record ucr
          ON obs.record_id = ucr.id::text
         AND obs.record_type = 'usda_census_record'
        JOIN public.usda_commodity uc ON ucr.commodity_code = uc.id
        JOIN public.place p ON ucr.geoid = p.geoid
        JOIN public.parameter param ON obs.parameter_id = param.id
        JOIN public.unit u ON obs.unit_id = u.id
        LEFT JOIN public.dimension_type dt ON obs.dimension_type_id = dt.id
        LEFT JOIN public.unit du ON obs.dimension_unit_id = du.id
        """
    )
    op.execute(
        f"""
        CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.usda_survey_view AS
        SELECT
          obs.id,
          uc.name AS usda_crop,
          p.geoid,
          param.name AS parameter,
          obs.value,
          u.name AS unit,
          dt.name AS dimension,
          obs.dimension_value,
          du.name AS dimension_unit
        FROM public.observation obs
        JOIN public.usda_survey_record usr
          ON obs.record_id = usr.id::text
         AND obs.record_type = 'usda_survey_record'
        JOIN public.usda_commodity uc ON usr.commodity_code = uc.id
        JOIN public.place p ON usr.geoid = p.geoid
        JOIN public.parameter param ON obs.parameter_id = param.id
        JOIN public.unit u ON obs.unit_id = u.id
        LEFT JOIN public.dimension_type dt ON obs.dimension_type_id = dt.id
        LEFT JOIN public.unit du ON obs.dimension_unit_id = du.id
        """
    )

    # Create analysis_average_view (depends on analysis_data_view)
    op.execute(
        f"CREATE MATERIALIZED VIEW {VIEW_SCHEMA}.analysis_average_view AS "
        f"{ANALYSIS_AVERAGE_VIEW_SQL}"
    )

    # Create spatial indexes
    for idx_name, view_name, column in SPATIAL_VIEW_INDEXES:
        op.execute(
            f"CREATE INDEX IF NOT EXISTS {idx_name} ON {VIEW_SCHEMA}.{view_name} "
            f"USING GIST ({column})"
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop materialized views in reverse order
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.analysis_average_view CASCADE")
    for view_name, _ in reversed(VIEW_DEFINITIONS):
        op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_SCHEMA}.{view_name} CASCADE")
