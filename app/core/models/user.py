from typing import TYPE_CHECKING, Optional

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)

from .user_group_association import user_group_association_table

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.types.user_id import UserIdType
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .group import Group
    from .task import Task


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    name: Mapped[str] = mapped_column(String(31))
    surname: Mapped[str] = mapped_column(String(31))
    patronymic: Mapped[Optional[str]] = mapped_column(String(63))

    groups: Mapped[list["Group"]] = relationship(
        secondary=user_group_association_table,
        back_populates="users",
    )

    admin_groups: Mapped[list["Group"]] = relationship(back_populates="admin")
    admin_tasks: Mapped[list["Task"]] = relationship(back_populates="admin")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
