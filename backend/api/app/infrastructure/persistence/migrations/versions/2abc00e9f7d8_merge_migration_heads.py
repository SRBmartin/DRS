"""Merge migration heads

Revision ID: 2abc00e9f7d8
Revises: 123456789dsx, 123456789abc
Create Date: 2025-03-18 20:11:59.900514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2abc00e9f7d8'
down_revision = ('123456789dsx', '123456789abc')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
