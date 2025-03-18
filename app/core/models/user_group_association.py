from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
)

from .base import Base

user_group_association_table = Table(
    "user_group_association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("group_id", ForeignKey("groups.id"), nullable=False),
    UniqueConstraint("user_id", "group_id", name="idx_user_group"),
)
