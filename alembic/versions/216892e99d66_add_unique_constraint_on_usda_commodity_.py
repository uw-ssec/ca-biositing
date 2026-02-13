"""Add unique constraint on usda_commodity.name

Revision ID: 216892e99d66
Revises: d8cf0b70462a
Create Date: 2026-02-13 11:37:57.617715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '216892e99d66'
down_revision: Union[str, Sequence[str], None] = 'd8cf0b70462a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add unique constraint on usda_commodity.name
    op.create_unique_constraint(
        'unique_usda_commodity_name',
        'usda_commodity',
        ['name']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the unique constraint
    op.drop_constraint(
        'unique_usda_commodity_name',
        'usda_commodity',
        type_='unique'
    )
