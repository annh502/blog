"""empty message

Revision ID: f91ac85e9fc0
Revises: 650b069cd1a0
Create Date: 2023-09-30 09:32:59.906689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f91ac85e9fc0'
down_revision = '650b069cd1a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('likes_user_id_fkey', 'likes', type_='foreignkey')
    op.drop_constraint('likes_post_id_fkey', 'likes', type_='foreignkey')
    op.drop_column('likes', 'post_id')
    op.drop_column('likes', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('likes', sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('likes_post_id_fkey', 'likes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('likes_user_id_fkey', 'likes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
