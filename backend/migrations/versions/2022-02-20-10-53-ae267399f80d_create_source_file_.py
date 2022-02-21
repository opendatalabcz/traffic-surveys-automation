"""Create source file and task tables.

Revision ID: ae267399f80d
Revises: 
Create Date: 2022-02-20 10:53:31.453256

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "ae267399f80d"
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
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("models", sa.ARRAY(sa.TEXT()), nullable=False),
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
        sa.ForeignKeyConstraint(["source_file_id"], ["source_file.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("output_path"),
    )


def downgrade():
    op.drop_table("task")
    op.drop_table("source_file")
