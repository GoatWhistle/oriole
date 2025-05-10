from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .assignment import Assignment
    from .user import User
    from .account import Account


class UserProfile(Base):

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    user: Mapped["User"] = relationship(back_populates="profile")

    accounts: Mapped[list["Account"]] = relationship(back_populates="user_profile")

    name: Mapped[str] = mapped_column(String(31), index=True)
    surname: Mapped[str] = mapped_column(String(31), index=True)
    patronymic: Mapped[str] = mapped_column(String(63), index=True)

    admin_assignments: Mapped[list["Assignment"]] = relationship(back_populates="admin")
