"""empty message

Revision ID: 5f1aa3268bad
Revises: ece890dd303c
Create Date: 2022-11-04 21:01:35.456630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1aa3268bad'
down_revision = 'ece890dd303c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('goal_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('goal_id', name='goal_pkey')
    )
    # ### end Alembic commands ###
