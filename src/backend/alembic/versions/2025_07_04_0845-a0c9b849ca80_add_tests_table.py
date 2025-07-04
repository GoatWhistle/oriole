"""add tests table

Revision ID: a0c9b849ca80
Revises: 267fdd7da2ae
Create Date: 2025-07-04 08:45:23.287298

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a0c9b849ca80"
down_revision: Union[str, None] = "267fdd7da2ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tests",
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("correct_output", sa.String(), nullable=False),
        sa.Column("input_data", sa.String(), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["code_tasks.id"],
            name=op.f("fk_tests_task_id_code_tasks"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tests")),
    )
    op.create_index(op.f("ix_tests_id"), "tests", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_tests_id"), table_name="tests")
    op.drop_table("tests")
