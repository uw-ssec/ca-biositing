"""Merge multiple heads

Revision ID: 64de60aff03d
Revises: cfe7ab7b7a20, fix_analysis_view_joins
Create Date: 2026-03-05 09:19:51.181996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64de60aff03d'
down_revision: Union[str, Sequence[str], None] = ('cfe7ab7b7a20', 'fix_analysis_view_joins')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
