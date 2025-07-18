from features.spaces.schemas import SpaceJoinStatusRead
from shared.enums.space_join_request import SpaceJoinStatusEnum


def build_space_join_status_read(
    status: SpaceJoinStatusEnum,
    user_id: int,
    space_id: int,
) -> SpaceJoinStatusRead:
    return SpaceJoinStatusRead(
        status=status.value,
        user_id=user_id,
        space_id=space_id,
    )
