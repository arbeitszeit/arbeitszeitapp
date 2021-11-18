"""add cooperation table and attributes to plan

Revision ID: bfe08c4388ae
Revises: 87a9fb39c257
Create Date: 2021-11-17 22:47:54.633044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bfe08c4388ae"
down_revision = "87a9fb39c257"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cooperation",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("definition", sa.String(length=5000), nullable=False),
        sa.Column("coordinator", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["coordinator"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "plan", sa.Column("requested_cooperation", sa.String(), nullable=True)
    )
    op.add_column("plan", sa.Column("cooperation", sa.String(), nullable=True))
    op.create_foreign_key(
        "plan_cooperation_fkey", "plan", "cooperation", ["cooperation"], ["id"]
    )
    op.create_foreign_key(
        "plan_requested_cooperation_fkey",
        "plan",
        "cooperation",
        ["requested_cooperation"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("plan_cooperation_fkey", "plan", type_="foreignkey")
    op.drop_constraint("plan_requested_cooperation_fkey", "plan", type_="foreignkey")
    op.drop_column("plan", "cooperation")
    op.drop_column("plan", "requested_cooperation")
    op.drop_table("cooperation")
    # ### end Alembic commands ###
