from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from features.groups.schemas import GroupInviteRead
from features.spaces.models import SpaceInvite
from shared.enums import SpaceTypeEnum


class GroupInvite(SpaceInvite):
    __mapper_args__ = {"polymorphic_identity": SpaceTypeEnum.GROUP.value}
    id: Mapped[int] = mapped_column(ForeignKey("space_invites.id"), primary_key=True)

    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)

    def get_validation_schema(self) -> GroupInviteRead:
        return GroupInviteRead.model_validate(self)
