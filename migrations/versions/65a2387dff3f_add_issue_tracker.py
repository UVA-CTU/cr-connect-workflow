"""add issue tracker

Revision ID: 65a2387dff3f
Revises: 23101c5facb4
Create Date: 2025-10-12 07:19:13.138711

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '65a2387dff3f'
down_revision = '23101c5facb4'
branch_labels = None
depends_on = None

def upgrade():
    """Add issue and issue_notes tables, along with enums."""

    op.create_table(
        'issue',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('customer', sa.Enum('ctu', 'researcher', 'uva', name='issuecustomer'), nullable=True),
        sa.Column('type', sa.Enum('bug', 'feature_request', 'support', name='issuetype'), nullable=True),
        sa.Column('status', sa.Enum('backlog', 'waiting', 'in_progress', 'resolved', 'closed', name='issuestatus'), nullable=False, server_default='backlog'),
        sa.Column('created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )

    op.create_table(
        'issue_notes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('issue_id', sa.Integer(), sa.ForeignKey('issue.id'), nullable=False),
        sa.Column('note', sa.Text(), nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('author', sa.String(length=255), nullable=False),
    )


def downgrade():
    """Drop issue and issue_notes tables, along with enums."""
    op.drop_table('issue_notes')
    op.drop_table('issue')

    op.execute('DROP TYPE IF EXISTS issuecustomer')
    op.execute('DROP TYPE IF EXISTS issuetype')
    op.execute('DROP TYPE IF EXISTS issuestatus')
