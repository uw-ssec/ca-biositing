"""recreate_mv_biomass_search_with_modular_approach

Recreate mv_biomass_search using the new modular data_portal_views package.
This is the first view to be recreated with immutable SQL snapshot at migration time.

Revision ID: 9e8f7a6b5c4e
Revises: 9e8f7a6b5c4d
Create Date: 2026-04-04 02:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from ca_biositing.datamodels.data_portal_views import mv_biomass_search


# revision identifiers, used by Alembic.
revision: str = '9e8f7a6b5c4e'
down_revision: Union[str, Sequence[str], None] = '9e8f7a6b5c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Recreate mv_biomass_search with the modular approach.

    This demonstrates the pattern for recreating views:
    1. Compile SQLAlchemy expression to SQL (immutable snapshot at migration time)
    2. Create the view with the compiled SQL
    3. Create unique index for performance
    4. Grant permissions to biocirv_readonly

    SQL Snapshot (immutable at migration time):
    - The compiled SQL below is the authoritative definition for this view
    - Changes to the SQLAlchemy expression in data_portal_views/mv_biomass_search.py
      require a new migration to update the view
    """
    # Compile the SQLAlchemy expression to SQL
    compiled = mv_biomass_search.compile(
        dialect=sa.dialects.postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )

    # Create the view with immutable SQL snapshot
    sql = f"""
    CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS
    {compiled}
    """
    op.execute(sql)

    # Create unique index for performance
    op.execute("""
    CREATE UNIQUE INDEX idx_mv_biomass_search_id
    ON data_portal.mv_biomass_search (id)
    """)

    # Grant select to readonly user
    op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")


def downgrade() -> None:
    """Downgrade: drop the view and index."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
