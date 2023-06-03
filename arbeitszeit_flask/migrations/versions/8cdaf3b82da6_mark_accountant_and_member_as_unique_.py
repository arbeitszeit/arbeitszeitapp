"""Mark Accountant and Member as unique per User

Revision ID: 8cdaf3b82da6
Revises: fb341bf85b13
Create Date: 2023-05-29 17:38:10.049850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cdaf3b82da6'
down_revision = 'fb341bf85b13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accountant', schema=None) as batch_op:
        batch_op.create_unique_constraint('accountant_user_id_key', ['user_id'])

    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.create_unique_constraint('member_user_id_key', ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.drop_constraint('member_user_id_key', type_='unique')

    with op.batch_alter_table('accountant', schema=None) as batch_op:
        batch_op.drop_constraint('accountant_user_id_key', type_='unique')

    # ### end Alembic commands ###