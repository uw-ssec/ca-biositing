"""Fix observation table constraint for multiple observations per record

Revision ID: d8cf0b70462a
Revises: 6fb7ecebb55f
Create Date: 2026-02-09 12:00:05.907986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8cf0b70462a'
down_revision: Union[str, Sequence[str], None] = '6fb7ecebb55f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Fix observation table constraint to allow multiple observations per record."""

    # Drop the incorrect unique constraint on record_id alone
    op.drop_constraint('observation_record_id_key', 'observation', type_='unique')

    # Add the correct composite unique constraint
    # This allows multiple observations per record (different parameters/units)
    # but prevents true duplicates
    op.create_unique_constraint(
        'observation_unique_key',
        'observation',
        ['record_id', 'record_type', 'parameter_id', 'unit_id']
    )


def downgrade() -> None:
    """Downgrade schema: Restore original single-column constraint."""

    # Drop the composite unique constraint
    op.drop_constraint('observation_unique_key', 'observation', type_='unique')

    # Restore the original single-column constraint
    # Note: This may fail if multiple observations per record exist
    op.create_unique_constraint(
        'observation_record_id_key',
        'observation',
        ['record_id']
    )
