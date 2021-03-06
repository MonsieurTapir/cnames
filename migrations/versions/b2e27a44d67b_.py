"""empty message

Revision ID: b2e27a44d67b
Revises: 4d450194f332
Create Date: 2018-01-11 22:52:02.378736

"""

# revision identifiers, used by Alembic.
revision = 'b2e27a44d67b'
down_revision = '4d450194f332'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('blue_score', sa.Integer(), nullable=True))
    op.add_column('rooms', sa.Column('red_score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'red_score')
    op.drop_column('rooms', 'blue_score')
    # ### end Alembic commands ###
