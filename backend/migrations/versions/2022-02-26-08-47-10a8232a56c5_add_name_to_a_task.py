"""Add name to a task.

Revision ID: 10a8232a56c5
Revises: c3d9c8da961a
Create Date: 2022-02-26 08:47:23.054288

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "10a8232a56c5"
down_revision = "c3d9c8da961a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("task", sa.Column("name", sa.TEXT(), nullable=False))
    op.alter_column(
        "task",
        "id",
        existing_type=sa.INTEGER(),
        nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('task_id_seq'::regclass)"),
    )


def downgrade():
    op.alter_column(
        "task",
        "id",
        existing_type=sa.INTEGER(),
        nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('task_id_seq'::regclass)"),
    )
    op.drop_column("task", "name")
