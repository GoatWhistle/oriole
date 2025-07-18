from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from features.users.schemas import UserProfileRead

if TYPE_CHECKING:
    from features.users.models import User
    from features.accounts.models import Account
    from features.spaces.models import Space, SpaceJoinRequest


class UserProfile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="profile")

    name: Mapped[str] = mapped_column(String(length=30), index=True)
    surname: Mapped[str] = mapped_column(String(length=30), index=True)
    patronymic: Mapped[str] = mapped_column(String(length=30), index=True)

    def get_validation_schema(self) -> UserProfileRead:
        return UserProfileRead.model_validate(self)

    accounts: Mapped[list["Account"]] = relationship(back_populates="user_profile")
    created_spaces: Mapped[list["Space"]] = relationship(back_populates="creator")
    space_join_requests: Mapped[list["SpaceJoinRequest"]] = relationship(
        back_populates="user_profile"
    )
