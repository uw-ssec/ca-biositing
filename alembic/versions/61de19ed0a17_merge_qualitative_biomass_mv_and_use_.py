"""merge qualitative biomass mv and use-case heads

Revision ID: 61de19ed0a17
Revises: 1bed1a9104a7, d2b6b2a7c9d1
Create Date: 2026-04-20 12:24:39.033675

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '61de19ed0a17'
down_revision: Union[str, Sequence[str], None] = ('1bed1a9104a7', 'd2b6b2a7c9d1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
