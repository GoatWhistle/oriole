from abc import abstractmethod
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.spaces.schemas import SpaceRead
from shared.enums import SpaceTypeEnum

if TYPE_CHECKING:
    from features.modules.models import Module
    from features.groups.models import GroupInvite
    from features.accounts.models import Account
    from features.users.models import UserProfile


class Space(Base, IdIntPkMixin):
    space_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    __mapper_args__ = {
        "polymorphic_identity": SpaceTypeEnum.BASE,
        "polymorphic_on": space_type,
        "with_polymorphic": "*",
    }

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))

    creator_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    creator: Mapped["UserProfile"] = relationship(back_populates="created_spaces")

    accounts: Mapped[list["Account"]] = relationship(back_populates="space")
    modules: Mapped[list["Module"]] = relationship(back_populates="space")
    invites: Mapped[list["GroupInvite"]] = relationship(back_populates="space")

    @abstractmethod
    def get_validation_schema(self) -> SpaceRead:
        return SpaceRead.model_validate(self)
