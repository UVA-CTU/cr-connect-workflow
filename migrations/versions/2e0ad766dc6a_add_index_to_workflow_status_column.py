"""add index to workflow status column

Revision ID: 2e0ad766dc6a
Revises: 23101c5facb4
Create Date: 2026-01-26 07:32:32.798984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0ad766dc6a'
down_revision = '23101c5facb4'
branch_labels = None
depends_on = None


def upgrade():
    """Add index to workflow status column"""
    # op.execute('ALTER TABLE table_name ADD INDEX index_name (column_name)')
    op.create_index('workflow_status_index',
                    'workflow',
                    ['status'], unique=False)
    op.create_index('workflow_state_index',
                    'workflow',
                    ['state'], unique=False)

def downgrade():
    """Revert index to workflow status column"""
    # op.execute('ALTER TABLE table_name DROP INDEX index_name')
    op.drop_index('workflow_status_index', 'workflow')
    op.drop_index('workflow_state_index', 'workflow')
