"""test_manual_no_auto

Revision ID: 76181497b8c2
Revises: 4cbe9009d2d8
Create Date: 2026-01-18 05:18:42.753518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76181497b8c2'
down_revision: Union[str, Sequence[str], None] = '4cbe9009d2d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
