"""empty message

Revision ID: beaf9b25be1f
Revises: 
Create Date: 2019-02-15 20:21:26.448583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beaf9b25be1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adminusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4'
    )
    op.create_index(op.f('ix_adminusers_username'), 'adminusers', ['username'], unique=True)
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('size', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_name', 'files', ['name'], unique=False)
    op.create_table('post_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_post_id', 'post_tags', ['post_id', 'updated_at'], unique=False)
    op.create_index('idx_tag_id', 'post_tags', ['tag_id', 'updated_at'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('intro', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('html_body', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_title', 'posts', ['title'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('idx_name', 'tags', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_name', table_name='tags')
    op.drop_table('tags')
    op.drop_index('idx_title', table_name='posts')
    op.drop_table('posts')
    op.drop_index('idx_tag_id', table_name='post_tags')
    op.drop_index('idx_post_id', table_name='post_tags')
    op.drop_table('post_tags')
    op.drop_index('idx_name', table_name='files')
    op.drop_table('files')
    op.drop_index(op.f('ix_adminusers_username'), table_name='adminusers')
    op.drop_table('adminusers')
    # ### end Alembic commands ###
