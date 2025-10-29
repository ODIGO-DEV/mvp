"""Add missing notes column to ingredients table

Revision ID: 1532ac7db848
Revises: 
Create Date: 2025-09-07 09:56:31.574881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1532ac7db848'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    op.drop_column('steps', 'duration')
    op.drop_column('steps', 'instruction')
    op.drop_column('steps', 'step_number')
    op.drop_column('ingredients', 'notes')