"""empty message

Revision ID: 384102feac86
Revises: 2d368018e3a3
Create Date: 2016-08-14 16:43:33.429000

"""

# revision identifiers, used by Alembic.
revision = '384102feac86'
down_revision = '2d368018e3a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comment_timestamp', 'comment', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_comment_timestamp', 'comment')
    op.drop_table('comment')
    ### end Alembic commands ###