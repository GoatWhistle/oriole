from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from utils import get_number_one_bit_less as get_num_opt

if TYPE_CHECKING:
    from features.modules.models import Module
    from features.users.models import User
    from features.groups.models import Account


class UserProfile(Base):

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    user: Mapped["User"] = relationship(back_populates="profile")

    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user_profile",
        cascade="all, delete-orphan",
    )

    name: Mapped[str] = mapped_column(String(length=get_num_opt(30)), index=True)
    surname: Mapped[str] = mapped_column(String(length=get_num_opt(30)), index=True)
    patronymic: Mapped[str] = mapped_column(String(length=get_num_opt(30)), index=True)

    admin_modules: Mapped[list["Module"]] = relationship(
        back_populates="admin",
        cascade="all, delete-orphan",
    )
