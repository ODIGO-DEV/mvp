"""Rename comment_text to content in Comment model

Revision ID: 1cb157e8d6ec
Revises: d6ee5dba23a3
Create Date: 2025-10-29 12:14:46.552557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb157e8d6ec'
down_revision = 'd6ee5dba23a3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=True))

    op.execute('UPDATE comments SET content = comment_text')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column('content', existing_type=sa.Text(), nullable=False)
        batch_op.drop_column('comment_text')


def downgrade():
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_text', sa.Text(), nullable=True))

    op.execute('UPDATE comments SET comment_text = content')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column('comment_text', existing_type=sa.Text(), nullable=False)
        batch_op.drop_column('content')