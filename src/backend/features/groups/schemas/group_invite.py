from urllib.parse import urljoin

from pydantic import Field, computed_field

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
    code: str = Field(exclude=True)

    @computed_field
    @property
    def url(self) -> str:
        base_url: str = self.__pydantic_context__.get(
            "base_url", "http://localhost:8000"
        )
        return urljoin(base_url, f"/groups/join/{self.code}")


class GroupInviteUpdate(GroupInviteBase, SpaceInviteUpdate):
    pass
