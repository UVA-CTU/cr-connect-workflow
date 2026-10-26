"""Add erroring workflow index

Revision ID: 9cf000c79688
Revises: a3f1c7b2e5d4
Create Date: 2026-10-26 11:16:41.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cf000c79688'
down_revision = 'a3f1c7b2e5d4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_workflow_erroring',
                    'workflow',
                    ['id'],
                    postgresql_where="status = 'erroring'")


def downgrade():
    op.drop_index('idx_workflow_erroring', 'workflow')