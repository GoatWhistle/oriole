"""Change int to datetime

Revision ID: 67e9ec5d837c
Revises: 4efff996de56
Create Date: 2025-05-25 16:52:27.490584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "67e9ec5d837c"
down_revision: Union[str, None] = "4efff996de56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Сначала убираем дефолтные значения
    op.alter_column("assignments", "start_datetime", server_default=None)
    op.alter_column("assignments", "end_datetime", server_default=None)
    op.alter_column("tasks", "start_datetime", server_default=None)
    op.alter_column("tasks", "end_datetime", server_default=None)

    # Затем изменяем тип
    op.alter_column(
        "assignments",
        "start_datetime",
        existing_type=sa.INTEGER(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="(timestamp 'epoch' + start_datetime * interval '1 second') AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "assignments",
        "end_datetime",
        existing_type=sa.INTEGER(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="(timestamp 'epoch' + end_datetime * interval '1 second') AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "group_invites",
        "expires_at",
        existing_type=sa.INTEGER(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="(timestamp 'epoch' + expires_at * interval '1 second') AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "tasks",
        "start_datetime",
        existing_type=sa.INTEGER(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="(timestamp 'epoch' + start_datetime * interval '1 second') AT TIME ZONE 'UTC'",
    )
    op.alter_column(
        "tasks",
        "end_datetime",
        existing_type=sa.INTEGER(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
        postgresql_using="(timestamp 'epoch' + end_datetime * interval '1 second') AT TIME ZONE 'UTC'",
    )

    # И только потом добавляем новые дефолтные значения
    op.alter_column("assignments", "start_datetime", server_default=sa.func.now())
    op.alter_column("assignments", "end_datetime", server_default=sa.func.now())
    op.alter_column("tasks", "start_datetime", server_default=sa.func.now())
    op.alter_column("tasks", "end_datetime", server_default=sa.func.now())


def downgrade() -> None:
    """Downgrade schema."""
    # Аналогичная логика для downgrade
    op.alter_column("tasks", "end_datetime", server_default=None)
    op.alter_column("tasks", "start_datetime", server_default=None)
    op.alter_column("group_invites", "expires_at", server_default=None)
    op.alter_column("assignments", "end_datetime", server_default=None)
    op.alter_column("assignments", "start_datetime", server_default=None)

    op.alter_column(
        "tasks",
        "end_datetime",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="FLOOR(EXTRACT(epoch FROM end_datetime))::integer",
    )
    op.alter_column(
        "tasks",
        "start_datetime",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="FLOOR(EXTRACT(epoch FROM start_datetime))::integer",
    )
    op.alter_column(
        "group_invites",
        "expires_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="FLOOR(EXTRACT(epoch FROM expires_at))::integer",
    )
    op.alter_column(
        "assignments",
        "end_datetime",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="FLOOR(EXTRACT(epoch FROM end_datetime))::integer",
    )
    op.alter_column(
        "assignments",
        "start_datetime",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="FLOOR(EXTRACT(epoch FROM start_datetime))::integer",
    )

    # Возвращаем дефолтные значения
    op.alter_column(
        "tasks",
        "end_datetime",
        server_default=sa.text("FLOOR(EXTRACT(epoch FROM now()))::integer"),
    )
    op.alter_column(
        "tasks",
        "start_datetime",
        server_default=sa.text("FLOOR(EXTRACT(epoch FROM now()))::integer"),
    )
    op.alter_column(
        "assignments",
        "end_datetime",
        server_default=sa.text("FLOOR(EXTRACT(epoch FROM now()))::integer"),
    )
    op.alter_column(
        "assignments",
        "start_datetime",
        server_default=sa.text("FLOOR(EXTRACT(epoch FROM now()))::integer"),
    )
