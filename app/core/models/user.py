from typing import TYPE_CHECKING, Optional

from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from .base import Base

from .user_group_association import user_group_association_table

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .group import Group
    from .task import Task


class User(Base, SQLAlchemyBaseUserTable[int]):
    # TODO: возможно потребуется изменить ->
    name: Mapped[str] = mapped_column(String(31))
    surname: Mapped[str] = mapped_column(String(31))
    patronymic: Mapped[str] = mapped_column(String(63))

    groups: Mapped[list[Optional["Group"]]] = relationship(
        secondary=user_group_association_table,
        back_populates="users",
    )

    admin_groups: Mapped[list[Optional["Group"]]] = relationship(back_populates="admin")

    admin_tasks: Mapped[list[Optional["Task"]]] = relationship(back_populates="admin")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
