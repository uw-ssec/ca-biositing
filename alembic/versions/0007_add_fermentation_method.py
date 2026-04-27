"""Add duration column to method table.

Revision ID: 0007a2cc5f91
Revises: d2b6b2a7c9d1
Create Date: 2026-04-27 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0007a2cc5f91"
down_revision: Union[str, Sequence[str], None] = "d2b6b2a7c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add nullable duration field to method records."""
    op.add_column("method", sa.Column("duration", sa.Float(), nullable=True))


def downgrade() -> None:
    """Remove duration field from method records."""
    op.drop_column("method", "duration")
