from pydantic import Field

from features.spaces.schemas import (
    SpaceInviteBase,
    SpaceInviteCreate,
    SpaceInviteRead,
    SpaceInviteUpdate,
)


class GroupInviteBase(SpaceInviteBase):
    pass


class GroupInviteCreate(GroupInviteBase, SpaceInviteCreate):
    pass


class GroupInviteRead(GroupInviteBase, SpaceInviteRead):
    code: str

    def to_with_link(self, link: str) -> "GroupInviteReadWithLink":
        return GroupInviteReadWithLink(**self.model_dump(), link=link)


class GroupInviteReadWithLink(GroupInviteRead):
    code: str = Field(exclude=True)
    link: str


class GroupInviteUpdate(GroupInviteBase, SpaceInviteUpdate):
    pass
