"""Create messages table

Revision ID: aaaffe6fa20b
Revises: 7b400eaf49d4
Create Date: 2025-06-25 11:20:55.560212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'aaaffe6fa20b'
down_revision: Union[str, None] = '7b400eaf49d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('messages',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('group_id', sa.Integer(), sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('sender_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('text', sa.Text(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
                    )

    op.create_index(op.f('ix_messages_group_id'), 'messages', ['group_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('messages')
