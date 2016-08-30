"""empty message

Revision ID: 9410f3396e4e
Revises: b511e26dc6a8
Create Date: 2016-08-29 22:25:28.799000

"""

# revision identifiers, used by Alembic.
revision = '9410f3396e4e'
down_revision = 'b511e26dc6a8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'new_avatar_default')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('new_avatar_default', sa.VARCHAR(length=32), nullable=True))
    ### end Alembic commands ###