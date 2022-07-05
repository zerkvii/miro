"""change usermenu to user_menu

Revision ID: 5c37c3a08b4c
Revises: 11258a2a13e9
Create Date: 2022-07-05 16:57:30.419669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c37c3a08b4c'
down_revision = '11258a2a13e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_menu_id'), 'user_menu', ['id'], unique=False)
    op.drop_index('ix_usermenu_id', table_name='usermenu')
    op.drop_table('usermenu')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usermenu',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('menu_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_usermenu_id', 'usermenu', ['id'], unique=False)
    op.drop_index(op.f('ix_user_menu_id'), table_name='user_menu')
    op.drop_table('user_menu')
    # ### end Alembic commands ###
