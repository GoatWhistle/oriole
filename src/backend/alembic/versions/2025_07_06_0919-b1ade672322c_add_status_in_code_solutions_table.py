"""add status in code solutions table

Revision ID: b1ade672322c
Revises: 82aeaa4f1ab9
Create Date: 2025-07-06 09:19:03.693310

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b1ade672322c"
down_revision: Union[str, None] = "82aeaa4f1ab9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "code_solutions",
        sa.Column("status", sa.String(), server_default="submitting", nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("code_solutions", "status")
