"""add code tasks model

Revision ID: 267fdd7da2ae
Revises: e4b002f2da08
Create Date: 2025-07-04 08:43:15.243222

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "267fdd7da2ae"
down_revision: Union[str, None] = "e4b002f2da08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "code_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("time_limit", sa.Integer(), nullable=False),
        sa.Column("memory_limit", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["tasks.id"],
            name=op.f("fk_code_tasks_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_code_tasks")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("code_tasks")
