"""Initial migration.

Revision ID: 3e690d4564e1
Revises: 
Create Date: 2021-11-17 19:50:22.265055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e690d4564e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('department', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_title', sa.Text(), nullable=False),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.Column('revenue', sa.Integer(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('vote_average', sa.REAL(), nullable=True),
    sa.Column('vote_count', sa.Integer(), nullable=True),
    sa.Column('overview', sa.Text(), nullable=True),
    sa.Column('tagline', sa.Text(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('release_date', sa.String(), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    op.drop_table('directors')
    # ### end Alembic commands ###
