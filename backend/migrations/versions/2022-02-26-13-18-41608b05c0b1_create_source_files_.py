"""Create source_files, tasks and lines tables.

Revision ID: 41608b05c0b1
Revises: 
Create Date: 2022-02-26 13:18:34.318575

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "41608b05c0b1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "source_files",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("path", sa.TEXT(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("new", "processing", "processed", "deleted", name="source_file_status"),
            server_default="new",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("models", sa.ARRAY(sa.TEXT()), nullable=False),
        sa.Column("output_method", sa.Enum("file", "video", name="task_output_method"), nullable=False),
        sa.Column("output_path", sa.TEXT(), nullable=False),
        sa.Column("parameters", sa.JSON(), server_default="{}", nullable=False),
        sa.Column(
            "status",
            sa.Enum("created", "processing", "completed", "failed", name="task_status"),
            server_default="created",
            nullable=False,
        ),
        sa.Column("source_file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_file_id"],
            ["source_files.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("output_path"),
    )
    op.create_index(op.f("ix_tasks_source_file_id"), "tasks", ["source_file_id"], unique=False)
    op.create_table(
        "lines",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("lines", sa.JSON(), server_default="{}", nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lines_task_id"), "lines", ["task_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_lines_task_id"), table_name="lines")
    op.drop_table("lines")
    op.drop_index(op.f("ix_tasks_source_file_id"), table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("source_files")
