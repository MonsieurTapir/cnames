"""empty message

Revision ID: 2854ca2aefdd
Revises: 7f94dba31ee3
Create Date: 2018-01-13 13:06:57.208846

"""

# revision identifiers, used by Alembic.
revision = '2854ca2aefdd'
down_revision = '7f94dba31ee3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('hotseat', sa.Boolean(), nullable=True))
    op.add_column('rooms', sa.Column('ongoing', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'ongoing')
    op.drop_column('rooms', 'hotseat')
    # ### end Alembic commands ###
