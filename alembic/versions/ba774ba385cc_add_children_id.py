"""add:children_id

Revision ID: ba774ba385cc
Revises: ac8f00033a08
Create Date: 2022-07-07 01:04:45.238347

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ba774ba385cc'
down_revision = 'ac8f00033a08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('menu', sa.Column('children_ids', mysql.SET(), nullable=True))
    # op.add_column('user_menu', sa.Column('children', mysql.SET(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_menu', 'children')
    op.drop_column('menu', 'children_ids')
    # ### end Alembic commands ###
