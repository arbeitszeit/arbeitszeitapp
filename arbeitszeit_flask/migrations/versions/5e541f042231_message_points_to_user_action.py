"""Message points to user action

Revision ID: 5e541f042231
Revises: 5f166cdf3014
Create Date: 2022-02-02 16:39:34.326536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e541f042231'
down_revision = '5f166cdf3014'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('user_action', sa.String(), nullable=True))
    op.create_foreign_key('message_user_action_fkey', 'message', 'user_action', ['user_action'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('message_user_action_fkey', 'message', type_='foreignkey')
    op.drop_column('message', 'user_action')
    # ### end Alembic commands ###