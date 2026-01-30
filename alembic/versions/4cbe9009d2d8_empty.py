"""empty

Revision ID: 4cbe9009d2d8
Revises: bb539f91106c
Create Date: 2026-01-18 03:28:57.958147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cbe9009d2d8'
down_revision: Union[str, Sequence[str], None] = 'bb539f91106c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
