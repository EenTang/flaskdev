"""empty message

Revision ID: b511e26dc6a8
Revises: 384102feac86
Create Date: 2016-08-29 22:03:25.603000

"""

# revision identifiers, used by Alembic.
revision = 'b511e26dc6a8'
down_revision = '384102feac86'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('new_avatar_default', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'new_avatar_default')
    ### end Alembic commands ###
