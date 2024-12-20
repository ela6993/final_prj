"""empty message

Revision ID: 93dd8dc8e38e
Revises: f6d17318cadf
Create Date: 2024-11-28 11:25:41.067183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93dd8dc8e38e'
down_revision = 'f6d17318cadf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('message_content', sa.Text(), nullable=False),
    sa.Column('chat_id', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('messages_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('message_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
