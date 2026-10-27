"""Add task_event workflow_id index

Revision ID: 950e374598b4
Revises: 9cf000c79688
Create Date: 2026-10-27 04:43:23.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '950e374598b4'
down_revision = '9cf000c79688'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_task_event_workflow_id',
                    'task_event',
                    ['workflow_id'])


def downgrade():
    op.drop_index('idx_task_event_workflow_id', 'task_event')
