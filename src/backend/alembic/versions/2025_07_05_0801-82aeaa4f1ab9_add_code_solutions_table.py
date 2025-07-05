"""add code solutions table

Revision ID: 82aeaa4f1ab9
Revises: 0033c3622eb4
Create Date: 2025-07-05 08:01:57.775638

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "82aeaa4f1ab9"
down_revision: Union[str, None] = "0033c3622eb4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "code_solutions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["solutions.id"],
            name=op.f("fk_code_solutions_id_solutions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_code_solutions")),
    )
    op.drop_column("solutions", "user_attempts")
    op.drop_column("solutions", "user_answer")
    op.add_column(
        "string_match_solutions",
        sa.Column("user_answer", sa.String(length=300), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("string_match_solutions", "user_answer")
    op.add_column(
        "solutions",
        sa.Column(
            "user_answer",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "solutions",
        sa.Column("user_attempts", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_table("code_solutions")
