"""add study_id index to workflow

Revision ID: e92ad72ed83e
Revises: 2e0ad766dc6a
Create Date: 2026-02-19 07:45:14.399471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e92ad72ed83e'
down_revision = '2e0ad766dc6a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('workflow_study_id_index', 'workflow', ['study_id'], unique=False)
    op.create_index('study_user_uid_index', 'study', ['user_uid'], unique=False)


def downgrade():
    op.drop_index('workflow_study_id_index', 'workflow')
    op.drop_index('study_user_uid_index', 'study')
