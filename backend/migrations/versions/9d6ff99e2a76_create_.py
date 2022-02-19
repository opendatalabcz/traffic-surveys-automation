"""Create source file and task tables.

Revision ID: 9d6ff99e2a76
Revises: 
Create Date: 2022-02-19 14:28:24.334267

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9d6ff99e2a76"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "source_file",
        sa.Column("name", sa.TEXT(), nullable=True),
        sa.Column("path", sa.TEXT(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("new", "processing", "processed", "deleted", name="source_file_status"),
            server_default="new",
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_table(
        "task",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("models", sa.ARRAY(sa.TEXT()), nullable=True),
        sa.Column("output_method", sa.Enum("file", "video", name="task_output_method"), nullable=False),
        sa.Column("output_path", sa.TEXT(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("created", "processing", "completed", "failed", name="task_status"),
            server_default="created",
            nullable=False,
        ),
        sa.Column("source_file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_file_id"],
            ["source_file.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("output_path"),
    )


def downgrade():
    op.drop_table("task")
    op.drop_table("source_file")
