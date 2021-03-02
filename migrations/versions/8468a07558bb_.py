"""empty message

Revision ID: 8468a07558bb
Revises: ebd5ce68a186
Create Date: 2021-03-01 20:03:13.707574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8468a07558bb'
down_revision = 'ebd5ce68a186'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('home_city', sa.String(), nullable=False))
    op.drop_column('teams', 'home_state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('home_state', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('teams', 'home_city')
    # ### end Alembic commands ###
