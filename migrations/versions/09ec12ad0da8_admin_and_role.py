"""admin and role

Revision ID: 09ec12ad0da8
Revises: 
Create Date: 2024-07-13 10:04:43.038886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09ec12ad0da8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_admin')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('password', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('last_login_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('current_login_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_login_ip', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('current_login_ip', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('login_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('confirmed_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.drop_index('ix_admin_adminname')
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=True)
        batch_op.drop_column('password_hash')
        batch_op.drop_column('adminname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adminname', sa.VARCHAR(length=64), nullable=False))
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True))
        batch_op.drop_index(batch_op.f('ix_admin_username'))
        batch_op.create_index('ix_admin_adminname', ['adminname'], unique=1)
        batch_op.alter_column('active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.drop_column('confirmed_at')
        batch_op.drop_column('login_count')
        batch_op.drop_column('current_login_ip')
        batch_op.drop_column('last_login_ip')
        batch_op.drop_column('current_login_at')
        batch_op.drop_column('last_login_at')
        batch_op.drop_column('password')
        batch_op.drop_column('username')

    op.create_table('_alembic_tmp_admin',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('active', sa.BOOLEAN(), nullable=False),
    sa.Column('fs_uniquifier', sa.VARCHAR(length=64), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('password', sa.VARCHAR(length=256), nullable=True),
    sa.Column('last_login_at', sa.DATETIME(), nullable=True),
    sa.Column('current_login_at', sa.DATETIME(), nullable=True),
    sa.Column('last_login_ip', sa.VARCHAR(length=100), nullable=True),
    sa.Column('current_login_ip', sa.VARCHAR(length=100), nullable=False),
    sa.Column('login_count', sa.INTEGER(), nullable=False),
    sa.Column('confirmed_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fs_uniquifier')
    )
    # ### end Alembic commands ###
