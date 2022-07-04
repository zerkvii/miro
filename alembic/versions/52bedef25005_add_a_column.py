"""Add a column

Revision ID: 52bedef25005
Revises: dcae97f6692e
Create Date: 2022-07-04 17:50:13.023276

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '52bedef25005'
down_revision = 'dcae97f6692e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
