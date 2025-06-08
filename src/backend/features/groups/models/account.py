from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import IdIntPkMixin
from database.base import Base

if TYPE_CHECKING:
    from features.users.models import UserProfile
    from features.groups.models import Group
    from features.tasks.models import UserReply


class Account(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    user_profile: Mapped["UserProfile"] = relationship(back_populates="accounts")

    role: Mapped[int] = mapped_column()

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="accounts")

    done_tasks: Mapped[list["UserReply"]] = relationship(back_populates="account")
