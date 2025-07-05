"""Add is_deleted column to survey table

Revision ID: 0bebabedac38
Revises: 2abc00e9f7d8
Create Date: 2025-03-18 20:14:35.111077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bebabedac38'
down_revision = '2abc00e9f7d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('surveys',
                  sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
                  schema='surveys'
                  )


def downgrade():
    op.drop_column('surveys', 'is_deleted', schema='surveys')
