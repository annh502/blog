"""empty message

Revision ID: 650b069cd1a0
Revises: 2a30687dad36
Create Date: 2023-09-29 16:21:35.356327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '650b069cd1a0'
down_revision = '2a30687dad36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###