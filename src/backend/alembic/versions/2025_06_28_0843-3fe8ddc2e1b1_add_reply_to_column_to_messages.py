"""Add reply_to column to messages

Revision ID: 3fe8ddc2e1b1
Revises: e7d5ad014471
Create Date: 2025-06-28 08:43:26.453075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3fe8ddc2e1b1'
down_revision: Union[str, None] = 'e7d5ad014471'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('messages', sa.Column('reply_to', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_messages_reply_to_messages',
        'messages', 'messages',
        ['reply_to'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_messages_reply_to_messages', 'messages', type_='foreignkey')
    op.drop_column('messages', 'reply_to')
