from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from features.groups.schemas import GroupInviteRead
from shared.enums import SpaceTypeEnum

if TYPE_CHECKING:
    from features.spaces.models import SpaceInvite


class GroupInvite(SpaceInvite):
    __mapper_args__ = {"polymorphic_identity": SpaceTypeEnum.GROUP.value}
    id: Mapped[int] = mapped_column(ForeignKey("space_invites.id"), primary_key=True)

    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)

    def get_validation_schema(self, base_url: str | None = None) -> GroupInviteRead:
        base_url = base_url or "http://localhost:8000"
        return GroupInviteRead.model_validate(self, context={"base_url": base_url})
