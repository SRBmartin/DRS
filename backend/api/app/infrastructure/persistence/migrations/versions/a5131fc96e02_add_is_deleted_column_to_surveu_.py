"""Add is_deleted column to surveu_responses table

Revision ID: a5131fc96e02
Revises: 0bebabedac38
Create Date: 2025-03-19 10:52:13.826171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5131fc96e02'
down_revision = '0bebabedac38'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('survey_responses',
                  sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
                  schema='surveys'
                  )


def downgrade():
    op.drop_column('survey_responses', 'is_deleted', schema='surveys')
