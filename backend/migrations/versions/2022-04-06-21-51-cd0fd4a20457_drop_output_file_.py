"""Drop output file type from database.

Revision ID: cd0fd4a20457
Revises: 41608b05c0b1
Create Date: 2022-04-06 21:51:27.162113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cd0fd4a20457"
down_revision = "41608b05c0b1"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("tasks", "output_method")
    op.execute("DROP TYPE IF EXISTS task_output_method")


def downgrade():
    op.add_column(
        "tasks",
        sa.Column(
            "output_method",
            postgresql.ENUM("file", "video", name="task_output_method"),
            autoincrement=False,
            nullable=False,
        ),
    )
