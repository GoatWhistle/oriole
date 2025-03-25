from typing import TYPE_CHECKING, Optional

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)
from sqlalchemy.orm import Mapped, relationship

from core.models.user_profile import UserProfile
from core.types.user_id import UserIdType
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    profile: Mapped["UserProfile"] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
