"""Adding User migration and User schema creation.

Revision ID: 4224411657a6
Revises: 
Create Date: 2024-11-17 13:39:01.541209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4224411657a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS users")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    schema='users'
    )

    op.create_table('session',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('started_time', sa.DateTime(), nullable=False),
    sa.Column('ending_time', sa.DateTime(), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='users'
    )
    # ### end Alembic commands ###


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS users")
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session', schema='users')
    op.drop_table('users', schema='users')
    # ### end Alembic commands ###