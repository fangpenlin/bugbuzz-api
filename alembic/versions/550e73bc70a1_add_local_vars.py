"""Add local_vars

Revision ID: 550e73bc70a1
Revises: None
Create Date: 2015-05-22 22:22:38.465302

"""

# revision identifiers, used by Alembic.
revision = '550e73bc70a1'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


def upgrade():
    op.add_column('breaks', sa.Column('local_vars', JSON), nullable=False)


def downgrade():
    op.drop_column('breaks', 'local_vars')
