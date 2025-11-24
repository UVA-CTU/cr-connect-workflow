"""get alembic up-to-date

Revision ID: 23101c5facb4
Revises: f1a12d1ef837
Create Date: 2025-10-11 16:19:10.872195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23101c5facb4'
down_revision = 'f1a12d1ef837'
branch_labels = None
depends_on = None

old_enum = sa.Enum('in_progress', 'hold', 'open_for_enrollment', 'abandoned',
                   name='studystatusenum')
new_enum = sa.Enum('in_progress', 'hold', 'open_for_enrollment', 'abandoned', 'cr_connect_complete',
                   name='studystatus')

def upgrade():
    op.alter_column('email_doc_codes','email_id',existing_type=sa.String(),nullable=False)
    op.alter_column('file','name',existing_type=sa.String(),nullable=False)
    op.alter_column('file','content_type',existing_type=sa.String(),nullable=False)
    op.drop_column('study', 'primary_investigator_id')
    op.drop_column('workflow', 'total_tasks')
    op.drop_column('workflow', 'completed_tasks')

    # Create new ENUM type
    new_enum.create(op.get_bind(), checkfirst=True)
    op.alter_column('study_event', 'status',
                    type_=new_enum,existing_type=old_enum,
                    existing_nullable=True,postgresql_using='status::text::studystatus')
    old_enum.drop(op.get_bind(), checkfirst=True)




def downgrade():
    op.alter_column('email_doc_codes','email_id',existing_type=sa.String(),nullable=True)
    op.alter_column('file','name',existing_type=sa.String(),nullable=True)
    op.alter_column('file','content_type',existing_type=sa.String(),nullable=True)
    op.add_column('study', sa.Column('primary_investigator_id', sa.Integer(), nullable=True))
    op.add_column('workflow', sa.Column('total_tasks', sa.Integer(), nullable=True))
    op.add_column('workflow', sa.Column('completed_tasks', sa.Integer(), nullable=True))

    # # Recreate old ENUM type
    # old_enum.create(op.get_bind(), checkfirst=True)
    # op.alter_column('study_event', 'status',
    #                 type_=old_enum,existing_type=new_enum,
    #                 existing_nullable=True,postgresql_using='status::text::studystatusenum')
    # new_enum.drop(op.get_bind(), checkfirst=True)
