"""update issue model

Revision ID: ddf5524d5a33
Revises: 65a2387dff3f
Create Date: 2025-10-12 09:22:45.577916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddf5524d5a33'
down_revision = '65a2387dff3f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('issue', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_issue_user_id_user',
        'issue', 'user',
        ['user_id'], ['id']
    )
    op.add_column('issue', sa.Column('assigned_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_issue_assigned_id_user',
        'issue', 'user',
        ['assigned_id'], ['id']
    )
    op.drop_column('issue_notes', 'author')
    op.add_column('issue_notes', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_issue_notes_author_id_user',
        'issue_notes', 'user',
        ['author_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_issue_assigned_id_user', 'issue', type_='foreignkey')
    op.drop_column('issue', 'assigned_id')
    op.drop_constraint('fk_issue_user_id_user', 'issue', type_='foreignkey')
    op.drop_column('issue', 'user_id')
    op.drop_constraint('fk_issue_notes_author_id_user', 'issue_notes', type_='foreignkey')
    op.drop_column('issue_notes', 'author_id')
    op.add_column('issue_notes', sa.Column('author', sa.String(length=255), nullable=False))
