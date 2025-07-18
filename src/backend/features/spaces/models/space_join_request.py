from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, IdIntPkMixin
from features.spaces.schemas import SpaceJoinRequestRead
from shared.enums import SpaceJoinRequestStatusEnum

if TYPE_CHECKING:
    from features.spaces.models import Space, SpaceInvite
    from features.users.models import UserProfile


class SpaceJoinRequest(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.user_id"))
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"))
    space_invite_id: Mapped[int | None] = mapped_column(ForeignKey("space_invites.id"))

    status: Mapped[str] = mapped_column(
        String(20), default=SpaceJoinRequestStatusEnum.PENDING.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.timezone("UTC", func.now())
    )

    def get_validation_schema(self) -> SpaceJoinRequestRead:
        return SpaceJoinRequestRead.model_validate(self)

    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="space_join_requests"
    )
    space: Mapped["Space"] = relationship(back_populates="space_join_requests")
    space_invite: Mapped["SpaceInvite"] = relationship(
        back_populates="space_join_requests"
    )
