"""Create ca_biositing schema

Revision ID: 90df744a03b4
Revises: fd64e8f83e51
Create Date: 2026-02-10 21:00:43.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90df744a03b4'
down_revision = 'ea01391d34c3'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS ca_biositing")


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS ca_biositing CASCADE")
