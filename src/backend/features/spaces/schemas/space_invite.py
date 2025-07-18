from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SpaceInviteBase(BaseModel):
    title: str | None = Field(default=None, max_length=100)

    expires_at: datetime | None = None
    max_usages: int | None = None

    needs_approval: bool = False


class SpaceInviteCreate(SpaceInviteBase):
    space_id: int


class SpaceInviteRead(SpaceInviteBase):
    id: int

    space_id: int
    creator_id: int

    created_at: datetime
    users_usages: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SpaceInviteUpdate(SpaceInviteBase):
    needs_approval: bool | None = None
