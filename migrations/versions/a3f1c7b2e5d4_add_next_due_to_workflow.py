"""Add next_due to workflow

Revision ID: a3f1c7b2e5d4
Revises: 833ae8c3717a
Create Date: 2026-08-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3f1c7b2e5d4'
down_revision = '833ae8c3717a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('workflow', sa.Column('next_due', sa.DateTime(timezone=True), nullable=True))
    op.create_index('idx_workflow_next_due',
                    'workflow',
                    ['next_due'],
                    postgresql_where="status = 'waiting'")


def downgrade():
    op.drop_index('idx_workflow_next_due', 'workflow')
    op.drop_column('workflow', 'next_due')
