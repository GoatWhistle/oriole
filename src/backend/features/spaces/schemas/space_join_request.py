from datetime import datetime

from pydantic import BaseModel, ConfigDict

from shared.enums import (
    SpaceJoinRequestStatusEnum,
    SpaceJoinStatusEnum,
    SpaceJoinRequestStatusUpdateEnum,
)


class SpaceJoinStatusRead(BaseModel):
    status: SpaceJoinStatusEnum
    user_id: int
    space_id: int


class SpaceJoinRequestBase(BaseModel):
    pass


class SpaceJoinRequestCreate(SpaceJoinRequestBase):
    user_id: int
    space_id: int
    space_invite_id: int


class SpaceJoinRequestRead(SpaceJoinRequestBase):
    id: int

    status: SpaceJoinRequestStatusEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SpaceJoinRequestUpdate(SpaceJoinRequestBase):
    status: SpaceJoinRequestStatusUpdateEnum | None = None
