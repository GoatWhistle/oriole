from typing import Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from features.spaces.models import SpaceJoinRequest
from features.spaces.schemas import SpaceJoinRequestCreate
from shared.enums import SpaceJoinRequestStatusEnum
from utils import get_current_utc


async def create_space_join_request(
    session: AsyncSession,
    space_join_request_create: SpaceJoinRequestCreate,
) -> SpaceJoinRequest:
    space_join_request = SpaceJoinRequest(
        **space_join_request_create.model_dump(),
        status=SpaceJoinRequestStatusEnum.PENDING,
        created_at=get_current_utc(),
    )
    session.add(space_join_request)
    await session.commit()
    await session.refresh(space_join_request)
    return space_join_request


async def get_space_join_request_by_id(
    session: AsyncSession,
    space_join_request_id: int,
) -> SpaceJoinRequest | None:
    return await session.get(SpaceJoinRequest, space_join_request_id)


async def get_space_join_request_by_user_id_and_space_id(
    session: AsyncSession,
    user_id: int,
    space_id: int,
) -> SpaceJoinRequest | None:
    statement = select(SpaceJoinRequest).where(
        SpaceJoinRequest.user_id == user_id, SpaceJoinRequest.space_id == space_id
    )
    result = await session.execute(statement)
    return result.scalars().first()


async def get_space_join_requests_by_space_id(
    session: AsyncSession,
    space_id: int,
    status: SpaceJoinRequestStatusEnum | None = None,
) -> list[SpaceJoinRequest]:
    statement = select(SpaceJoinRequest).where(SpaceJoinRequest.space_id == space_id)
    if status is not None:
        statement = statement.where(SpaceJoinRequest.status == status)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def update_space_join_request(
    session: AsyncSession,
    space_join_request: SpaceJoinRequest,
    update_data: dict[str, Any],
) -> SpaceJoinRequest:
    for key, value in update_data.items():
        setattr(space_join_request, key, value)
    await session.commit()
    await session.refresh(space_join_request)
    return space_join_request


async def delete_space_join_request(
    session: AsyncSession,
    space_join_request: SpaceJoinRequest,
) -> None:
    await session.delete(space_join_request)
    await session.commit()


async def delete_space_join_requests_by_space_id(
    session: AsyncSession,
    space_id: int,
    status: SpaceJoinRequestStatusEnum | None = None,
) -> None:
    statement = delete(SpaceJoinRequest).where(SpaceJoinRequest.space_id == space_id)
    if status is not None:
        statement = statement.where(SpaceJoinRequest.status == status)
    await session.execute(statement)
    await session.commit()
