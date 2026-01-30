"""Change Polygon geom to geometry type

Revision ID: 51167f08e5d5
Revises: 4f28299e735d
Create Date: 2026-01-20 14:22:31.109904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51167f08e5d5'
down_revision: Union[str, Sequence[str], None] = '4f28299e735d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Drop the dependent foreign key first
    op.drop_constraint('landiq_record_polygon_id_fkey', 'landiq_record', type_='foreignkey')

    # 2. Drop the unique constraint that is being changed
    op.drop_constraint('uq_polygon_geom', 'polygon', type_='unique')

    # 3. Re-create the unique constraint on geom (it's still Text in DB until we do a real type change,
    # but LinkML might have just wanted to refresh it. Actually, LinkML didn't change the DB type yet.)
    op.create_unique_constraint('uq_polygon_geom', 'polygon', ['geom'])

    # 4. Re-create the foreign key
    op.create_foreign_key('landiq_record_polygon_id_fkey', 'landiq_record', 'polygon', ['polygon_id'], ['geom'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('landiq_record_polygon_id_fkey', 'landiq_record', type_='foreignkey')
    op.drop_constraint('uq_polygon_geom', 'polygon', type_='unique')
    op.create_unique_constraint('uq_polygon_geom', 'polygon', ['geom'])
    op.create_foreign_key('landiq_record_polygon_id_fkey', 'landiq_record', 'polygon', ['polygon_id'], ['geom'])
