from sqlalchemy.ext.asyncio import AsyncSession

import features.accounts.crud.account as account_crud
import features.spaces.crud.space_join_request as space_join_request_crud
from features.accounts.schemas import AccountRole
from features.groups.validators import (
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.spaces.schemas import SpaceJoinRequestRead, SpaceJoinRequestUpdate
from features.spaces.validators.existence import (
    get_space_or_404,
    get_space_join_request_or_404,
)
from shared.enums import SpaceJoinRequestStatusEnum


async def get_space_join_request_by_id(
    session: AsyncSession,
    user_id: int,
    space_join_request_id: int,
) -> SpaceJoinRequestRead:
    space_join_request = await get_space_join_request_or_404(
        session, space_join_request_id
    )
    _ = await get_space_or_404(session, space_join_request.space_id)
    account = await get_account_or_404(session, user_id, space_join_request.space_id)

    check_user_is_admin_or_owner(account.role)

    return space_join_request.get_validation_schema()


async def get_space_join_requests_by_space_id(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    status: SpaceJoinRequestStatusEnum | None = None,
) -> list[SpaceJoinRequestRead]:
    _ = await get_space_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    check_user_is_admin_or_owner(account.role)

    space_join_requests = (
        await space_join_request_crud.get_space_join_requests_by_space_id(
            session, space_id, status
        )
    )
    return [
        space_join_request.get_validation_schema()
        for space_join_request in space_join_requests
    ]


async def update_space_join_request(
    session: AsyncSession,
    user_id: int,
    space_join_request_id: int,
    space_join_request_update: SpaceJoinRequestUpdate,
) -> SpaceJoinRequestRead:
    space_join_request = await get_space_join_request_or_404(
        session, space_join_request_id
    )
    _ = await get_space_or_404(session, space_join_request.space_id)
    account = await get_account_or_404(session, user_id, space_join_request.space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = space_join_request_update.model_dump(exclude_unset=True)

    space_join_request = await space_join_request_crud.update_space_join_request(
        session, space_join_request, update_data
    )
    if space_join_request.status == SpaceJoinRequestStatusEnum.APPROVED:
        await account_crud.create_account(
            session,
            space_join_request.user_id,
            space_join_request.space_id,
            AccountRole.MEMBER.value,
        )

    return space_join_request.get_validation_schema()


async def update_space_join_requests_by_space_id(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    space_join_request_update: SpaceJoinRequestUpdate,
) -> list[SpaceJoinRequestRead]:
    _ = await get_space_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    check_user_is_admin_or_owner(account.role)

    update_data = space_join_request_update.model_dump(exclude_unset=True)

    space_join_requests = (
        await space_join_request_crud.get_space_join_requests_by_space_id(
            session, space_id, SpaceJoinRequestStatusEnum.PENDING
        )
    )

    updated_requests = []

    for request in space_join_requests:
        updated = await space_join_request_crud.update_space_join_request(
            session, request, update_data
        )
        updated_requests.append(updated)

        if updated.status == SpaceJoinRequestStatusEnum.APPROVED:
            await account_crud.create_account(
                session, updated.user_id, updated.space_id, AccountRole.MEMBER.value
            )

    return [
        space_join_request.get_validation_schema()
        for space_join_request in updated_requests
    ]


async def delete_space_join_request(
    session: AsyncSession,
    user_id: int,
    space_join_request_id: int,
) -> None:
    space_join_request = await get_space_join_request_or_404(
        session, space_join_request_id
    )
    _ = await get_space_or_404(session, space_join_request.space_id)
    account = await get_account_or_404(session, user_id, space_join_request.space_id)

    check_user_is_admin_or_owner(account.role)

    await space_join_request_crud.delete_space_join_request(session, space_join_request)


async def delete_space_join_requests_by_space_id(
    session: AsyncSession,
    user_id: int,
    space_id: int,
    status: SpaceJoinRequestStatusEnum | None = None,
) -> None:
    _ = await get_space_or_404(session, space_id)
    account = await get_account_or_404(session, user_id, space_id)

    check_user_is_admin_or_owner(account.role)

    await space_join_request_crud.delete_space_join_requests_by_space_id(
        session, space_id, status
    )
