from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.accounts.services import account as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.patch(
    "/{space_id}/promote/{promote_user_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def promote_user_to_admin(
    promote_user_id: int,
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.promote_user_to_admin(
        session, user_id, promote_user_id, space_id
    )
    return create_json_response(data=data)


@router.patch(
    "/{space_id}/demote/{demote_user_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def demote_user_to_member(
    demote_user_id: int,
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.demote_user_to_member(
        session, user_id, demote_user_id, space_id
    )
    return create_json_response(data=data)


@router.delete(
    "/{space_id}/kick/{remove_user_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def remove_user_from_space(
    remove_user_id: int,
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.remove_user_from_space(session, user_id, remove_user_id, space_id)


@router.delete(
    "/{space_id}/leave/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def leave_from_space(
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.leave_from_space(session, user_id, space_id)


@router.get(
    "/{space_id}/users/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_accounts_in_space(
    request: Request,
    space_id: int,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_accounts_in_space(session, user_id, space_id)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/spaces/{space_id}/users/",
    )
