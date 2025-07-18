from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.spaces.schemas import SpaceInviteRead
from shared.enums import SpaceTypeEnum

if TYPE_CHECKING:
    from features.accounts.models import Account
    from features.spaces.models import Space, SpaceJoinRequest


class SpaceInvite(Base, IdIntPkMixin):
    space_invite_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )

    __mapper_args__ = {
        "polymorphic_identity": SpaceTypeEnum.BASE,
        "polymorphic_on": space_invite_type,
        "with_polymorphic": "*",
    }

    title: Mapped[str] = mapped_column(String(100))

    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    max_usages: Mapped[int | None] = mapped_column(nullable=True)
    users_usages: Mapped[int] = mapped_column(default=0)

    is_active: Mapped[bool] = mapped_column(default=True)

    needs_approval: Mapped[bool] = mapped_column(default=False)

    @abstractmethod
    def get_validation_schema(self) -> SpaceInviteRead:
        return SpaceInviteRead.model_validate(self)

    space: Mapped["Space"] = relationship(back_populates="invites")
    creator: Mapped["Account"] = relationship(back_populates="created_space_invites")
    space_join_requests: Mapped[list["SpaceJoinRequest"]] = relationship(
        back_populates="space_invite"
    )
