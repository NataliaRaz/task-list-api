"""create goals table

Revision ID: 506462e10b18
Revises: 0705f890e970
Create Date: 2025-05-08 10:21:14.325196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '506462e10b18'
down_revision = '0705f890e970'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('goal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='goal_pkey')
    )
    op.drop_table('goals')
    # ### end Alembic commands ###
