"""Add waiting workflow index

Revision ID: 833ae8c3717a
Revises: e92ad72ed83e
Create Date: 2026-06-10 06:34:37.840588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '833ae8c3717a'
down_revision = 'e92ad72ed83e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_workflow_waiting_ordered',
                    'workflow',
                    ['last_updated', 'study_id'],
                    postgresql_where="status = 'waiting'")


def downgrade():
    op.drop_index('idx_workflow_waiting_ordered', 'workflow')
