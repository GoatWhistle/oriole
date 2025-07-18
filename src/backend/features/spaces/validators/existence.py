from sqlalchemy.ext.asyncio import AsyncSession

import features.spaces.crud.space as space_crud
import features.spaces.crud.space_join_request as space_join_request_crud
from features.spaces.exceptions import (
    SpaceNotFoundException,
    SpaceJoinRequestNotFoundException,
)
from features.spaces.models import Space, SpaceJoinRequest


async def get_space_or_404(
    session: AsyncSession,
    space_id: int,
) -> Space:
    space = await space_crud.get_space_by_id(session, space_id)
    if not space:
        raise SpaceNotFoundException()
    return space


async def get_space_join_request_or_404(
    session: AsyncSession,
    space_join_request_id: int,
) -> SpaceJoinRequest:
    space_join_request = await space_join_request_crud.get_space_join_request_by_id(
        session, space_join_request_id
    )
    if not space_join_request:
        raise SpaceJoinRequestNotFoundException()
    return space_join_request


async def is_space_join_requests_exists(
    session: AsyncSession,
    user_id: int,
    space_id: int,
) -> bool:
    space_join_request = (
        await space_join_request_crud.get_space_join_request_by_user_id_and_space_id(
            session, user_id, space_id
        )
    )
    return True if space_join_request else False
