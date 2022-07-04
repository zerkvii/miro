"""drop table acount

Revision ID: 4941b208ba3b
Revises: 754dc0f21734
Create Date: 2022-07-04 23:37:32.479641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4941b208ba3b'
down_revision = '754dc0f21734'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('account')
    pass


def downgrade() -> None:
    pass
