"""drop user

Revision ID: 6d36b07ad371
Revises: ac6d51e69a88
Create Date: 2022-07-10 05:03:59.915493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d36b07ad371'
down_revision = 'ac6d51e69a88'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # pass
    op.drop_table('user_menu')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###