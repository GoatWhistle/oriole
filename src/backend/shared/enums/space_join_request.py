from enum import Enum


class SpaceJoinStatusEnum(str, Enum):
    ALREADY_JOINED = "already_joined"
    ALREADY_REQUESTED = "already_requested"
    JOINED = "joined"
    REQUESTED = "requested"


class SpaceJoinRequestStatusUpdateEnum(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


class SpaceJoinRequestStatusEnum(SpaceJoinRequestStatusUpdateEnum):
    PENDING = "pending"
