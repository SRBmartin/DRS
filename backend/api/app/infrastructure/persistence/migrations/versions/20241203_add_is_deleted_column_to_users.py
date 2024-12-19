"""Adding is_deleted field to users table.

Revision ID: 123456789abc
Revises: 4224411657a6
Create Date: 2024-12-03 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = '123456789abc'
down_revision = '4224411657a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        schema='users'
    )



def downgrade():
    op.drop_column('users', 'is_deleted', schema='users')
