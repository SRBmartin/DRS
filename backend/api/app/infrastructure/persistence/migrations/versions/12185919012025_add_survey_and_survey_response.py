"""Adding User migration and User schema creation.

Revision ID: 12185919012025
Revises: 
Create Date: 2025-01-19 00:18:59.545809
"""

from alembic import op
import sqlalchemy as sa

revision = '12185919012025'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS surveys")
    op.create_table('surveys',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('question', sa.String(length=1000), nullable=False),
        sa.Column('created_time', sa.DateTime(), nullable=False),
        sa.Column('ending_time', sa.DateTime(), nullable=False),
        sa.Column('is_anonymous', sa.Boolean(), nullable=False),
        sa.Column('user_ended', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='surveys'
    )
    op.create_table('survey_responses',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('survey_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('response', sa.String(length=32), nullable=False, server_default="no response"),
        sa.Column('responded_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], ),
        sa.ForeignKeyConstraint(['survey_id'], ['surveys.surveys.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='surveys'
    )

def downgrade():
    op.drop_table('surveys', schema='surveys')
    op.drop_table('survey_responses', schema='surveys')
    op.execute("DROP SCHEMA IF EXISTS surveys")
