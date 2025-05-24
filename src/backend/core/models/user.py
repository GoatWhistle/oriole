from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Boolean

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_profile import UserProfile


class User(Base, IdIntPkMixin):
    email: Mapped[str] = mapped_column(
        String(length=127), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1023), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
