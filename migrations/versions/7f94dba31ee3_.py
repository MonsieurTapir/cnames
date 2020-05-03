"""empty message

Revision ID: 7f94dba31ee3
Revises: e6cc6d3ed652
Create Date: 2018-01-12 15:15:44.197659

"""

# revision identifiers, used by Alembic.
revision = '7f94dba31ee3'
down_revision = 'e6cc6d3ed652'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('blue_to_guess', sa.Integer(), nullable=True))
    op.add_column('rooms', sa.Column('hint_word', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('red_to_guess', sa.Integer(), nullable=True))
    op.add_column('rooms', sa.Column('remaining_guesses', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'remaining_guesses')
    op.drop_column('rooms', 'red_to_guess')
    op.drop_column('rooms', 'hint_word')
    op.drop_column('rooms', 'blue_to_guess')
    # ### end Alembic commands ###