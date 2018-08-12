"""empty message

Revision ID: 082497676d81
Revises: 53ea11bf28de
Create Date: 2018-07-17 20:10:20.371991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082497676d81'
down_revision = '53ea11bf28de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('code', sa.String(length=8), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verifications')
    # ### end Alembic commands ###