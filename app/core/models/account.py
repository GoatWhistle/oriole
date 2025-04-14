from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .user_profile import UserProfile
    from .group import Group
    from .task import Task


class Account(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    user_profile: Mapped["UserProfile"] = relationship(back_populates="accounts")

    role: Mapped[int] = mapped_column()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="accounts")

    done_tasks: Mapped[list["Task"]] = relationship(back_populates="account")
