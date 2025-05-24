"""Change datetime to timestamp

Revision ID: 4efff996de56
Revises: 95160571b5fb
Create Date: 2025-05-23 21:45:58.098314

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4efff996de56"
down_revision: Union[str, None] = "95160571b5fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        "fk_access_tokens_user_id_users", "access_tokens", type_="foreignkey"
    )

    op.drop_table("access_tokens")

    columns_to_convert = [
        ("assignments", "start_datetime"),
        ("assignments", "end_datetime"),
        ("tasks", "start_datetime"),
        ("tasks", "end_datetime"),
        ("group_invites", "expires_at"),
    ]

    for table, column in columns_to_convert:
        if column != "expires_at":
            op.alter_column(
                table,
                column,
                server_default=None,
                existing_type=postgresql.TIMESTAMP(),
                existing_nullable=False,
            )

    for table, column in columns_to_convert:
        op.alter_column(
            table,
            column,
            type_=sa.Integer(),
            postgresql_using=f"EXTRACT(EPOCH FROM {column})::integer",
            nullable=False,
        )

    for table, column in [
        ("assignments", "start_datetime"),
        ("assignments", "end_datetime"),
        ("tasks", "start_datetime"),
        ("tasks", "end_datetime"),
    ]:
        op.alter_column(
            table, column, server_default=sa.text("EXTRACT(EPOCH FROM now())::integer")
        )


def downgrade() -> None:
    """Downgrade schema."""
    for table, column in [
        ("tasks", "end_datetime"),
        ("tasks", "start_datetime"),
        ("assignments", "end_datetime"),
        ("assignments", "start_datetime"),
    ]:
        op.alter_column(
            table,
            column,
            server_default=None,
            existing_type=sa.Integer(),
            existing_nullable=False,
        )

    op.alter_column(
        "tasks",
        "end_datetime",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="to_timestamp(end_datetime) AT TIME ZONE 'UTC'",
        nullable=False,
        server_default=sa.text("now()"),
    )
    op.alter_column(
        "tasks",
        "start_datetime",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="to_timestamp(start_datetime) AT TIME ZONE 'UTC'",
        nullable=False,
        server_default=sa.text("now()"),
    )
    op.alter_column(
        "group_invites",
        "expires_at",
        type_=postgresql.TIMESTAMP(),
        postgresql_using="to_timestamp(expires_at)",
        nullable=False,
    )
    op.alter_column(
        "assignments",
        "end_datetime",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="to_timestamp(end_datetime) AT TIME ZONE 'UTC'",
        nullable=False,
        server_default=sa.text("now()"),
    )
    op.alter_column(
        "assignments",
        "start_datetime",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="to_timestamp(start_datetime) AT TIME ZONE 'UTC'",
        nullable=False,
        server_default=sa.text("now()"),
    )

    op.create_table(
        "access_tokens",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "token",
            sa.VARCHAR(length=511),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("created_at", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_access_tokens_user_id_users"
        ),
        sa.PrimaryKeyConstraint("user_id", name="pk_access_tokens"),
    )
