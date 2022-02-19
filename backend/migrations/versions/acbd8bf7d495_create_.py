"""Create source file and task tables.

Revision ID: acbd8bf7d495
Revises: 
Create Date: 2022-02-19 09:41:31.426123

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "acbd8bf7d495"
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
    )


def downgrade():
    op.drop_table("task")
    op.drop_table("source_file")
