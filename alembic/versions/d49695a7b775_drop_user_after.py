"""drop user after

Revision ID: d49695a7b775
Revises: 467b7fdf5c44
Create Date: 2022-07-18 16:40:59.318836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd49695a7b775'
down_revision = '467b7fdf5c44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('children_ids', sa.String(length=32), nullable=True),
    sa.Column('meta', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_menu_id'), 'menu', ['id'], unique=False)
    op.create_index(op.f('ix_menu_name'), 'menu', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('hashed_password', sa.String(length=64), nullable=False),
    sa.Column('avatar', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=128), nullable=True),
    sa.Column('registrationDate', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('job', sa.String(length=128), nullable=True),
    sa.Column('organization', sa.String(length=128), nullable=True),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('introduction', sa.String(length=128), nullable=True),
    sa.Column('personalWebsite', sa.String(length=128), nullable=True),
    sa.Column('jobName', sa.String(length=128), nullable=True),
    sa.Column('organizationName', sa.String(length=128), nullable=True),
    sa.Column('locationName', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('user_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('menu_order', sa.Integer(), nullable=True),
    sa.Column('children_ids', sa.String(length=32), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'menu_id', name='uix_1')
    )
    op.create_index(op.f('ix_user_menu_id'), 'user_menu', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_menu_id'), table_name='user_menu')
    op.drop_table('user_menu')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_menu_name'), table_name='menu')
    op.drop_index(op.f('ix_menu_id'), table_name='menu')
    op.drop_table('menu')
    # ### end Alembic commands ###