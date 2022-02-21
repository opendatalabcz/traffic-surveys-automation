"""Create lines table.

Revision ID: c3d9c8da961a
Revises: ae267399f80d
Create Date: 2022-02-20 11:06:43.665566

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c3d9c8da961a"
down_revision = "ae267399f80d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "lines",
        sa.Column("lines", sa.JSON(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.ForeignKeyConstraint(["task_id"], ["task.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("lines")
