"""Enable uuid-ossp and create survey_sent_emails table

Revision ID: 123456789gfd
Revises: 12185919012025
Create Date: 2025-02-01 14:22:15:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '123456789dsx'
down_revision = '12185919012025'
branch_labels = None
depends_on = None

def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.execute("CREATE SCHEMA IF NOT EXISTS email")

    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 
            FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'emailstatus' 
              AND n.nspname = 'email'
        ) THEN
            EXECUTE 'CREATE TYPE email.emailstatus AS ENUM (''PENDING'', ''SENT'', ''FAILED'')';
        END IF;
    END$$;
    """)

    email_status_enum = sa.Enum(
        'PENDING', 'SENT', 'FAILED',
        name='email.emailstatus',
        create_type=False,
    )

    op.create_table(
        'survey_sent_emails',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True),
                  primary_key=True, nullable=False,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column('survey_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('status', email_status_enum, nullable=False, server_default='PENDING'),
        sa.Column('status_change_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['survey_id'], ['surveys.surveys.id']),
        schema='email'
    )

def downgrade():
    op.drop_table('survey_sent_emails', schema='email')
    op.execute("DROP TYPE IF EXISTS email.emailstatus")
    op.execute("DROP SCHEMA IF EXISTS email")
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
