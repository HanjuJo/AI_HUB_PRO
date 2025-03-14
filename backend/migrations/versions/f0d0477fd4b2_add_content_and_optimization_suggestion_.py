"""Add content and optimization suggestion models

Revision ID: f0d0477fd4b2
Revises: 
Create Date: 2025-03-14 00:04:31.468687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0d0477fd4b2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aitool',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('pricing_type', sa.String(length=50), nullable=True),
    sa.Column('pricing_details', sa.Text(), nullable=True),
    sa.Column('features', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aitool_id'), 'aitool', ['id'], unique=False)
    op.create_index(op.f('ix_aitool_name'), 'aitool', ['name'], unique=False)
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('recommendedchannel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.String(length=100), nullable=False),
    sa.Column('channel_name', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recommendedchannel_channel_id'), 'recommendedchannel', ['channel_id'], unique=True)
    op.create_index(op.f('ix_recommendedchannel_id'), 'recommendedchannel', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('youtubechannel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.String(length=100), nullable=False),
    sa.Column('channel_name', sa.String(length=100), nullable=True),
    sa.Column('subscriber_count', sa.Integer(), nullable=True),
    sa.Column('video_count', sa.Integer(), nullable=True),
    sa.Column('is_monetized', sa.Boolean(), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_youtubechannel_channel_id'), 'youtubechannel', ['channel_id'], unique=True)
    op.create_index(op.f('ix_youtubechannel_id'), 'youtubechannel', ['id'], unique=False)
    op.create_table('youtubedata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=100), nullable=False),
    sa.Column('popularity_score', sa.Float(), nullable=True),
    sa.Column('search_volume', sa.Integer(), nullable=True),
    sa.Column('is_trending', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_youtubedata_id'), 'youtubedata', ['id'], unique=False)
    op.create_index(op.f('ix_youtubedata_keyword'), 'youtubedata', ['keyword'], unique=False)
    op.create_table('content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('content_type', sa.String(length=50), nullable=True),
    sa.Column('keywords', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('seo_score', sa.Float(), nullable=True),
    sa.Column('meta_description', sa.String(length=300), nullable=True),
    sa.Column('meta_keywords', sa.String(length=200), nullable=True),
    sa.Column('readability_score', sa.Float(), nullable=True),
    sa.Column('engagement_score', sa.Float(), nullable=True),
    sa.Column('technical_score', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_id'), 'content', ['id'], unique=False)
    op.create_index(op.f('ix_content_title'), 'content', ['title'], unique=False)
    op.create_table('tool_categories',
    sa.Column('tool_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['tool_id'], ['aitool.id'], ),
    sa.PrimaryKeyConstraint('tool_id', 'category_id')
    )
    op.create_table('toolcombination',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('content_type', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_toolcombination_id'), 'toolcombination', ['id'], unique=False)
    op.create_table('combination_tools',
    sa.Column('combination_id', sa.Integer(), nullable=False),
    sa.Column('tool_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['combination_id'], ['toolcombination.id'], ),
    sa.ForeignKeyConstraint(['tool_id'], ['aitool.id'], ),
    sa.PrimaryKeyConstraint('combination_id', 'tool_id')
    )
    op.create_table('optimizationsuggestion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('suggestion', sa.Text(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('implemented', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_optimizationsuggestion_id'), 'optimizationsuggestion', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_optimizationsuggestion_id'), table_name='optimizationsuggestion')
    op.drop_table('optimizationsuggestion')
    op.drop_table('combination_tools')
    op.drop_index(op.f('ix_toolcombination_id'), table_name='toolcombination')
    op.drop_table('toolcombination')
    op.drop_table('tool_categories')
    op.drop_index(op.f('ix_content_title'), table_name='content')
    op.drop_index(op.f('ix_content_id'), table_name='content')
    op.drop_table('content')
    op.drop_index(op.f('ix_youtubedata_keyword'), table_name='youtubedata')
    op.drop_index(op.f('ix_youtubedata_id'), table_name='youtubedata')
    op.drop_table('youtubedata')
    op.drop_index(op.f('ix_youtubechannel_id'), table_name='youtubechannel')
    op.drop_index(op.f('ix_youtubechannel_channel_id'), table_name='youtubechannel')
    op.drop_table('youtubechannel')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_recommendedchannel_id'), table_name='recommendedchannel')
    op.drop_index(op.f('ix_recommendedchannel_channel_id'), table_name='recommendedchannel')
    op.drop_table('recommendedchannel')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_aitool_name'), table_name='aitool')
    op.drop_index(op.f('ix_aitool_id'), table_name='aitool')
    op.drop_table('aitool')
    # ### end Alembic commands ###
