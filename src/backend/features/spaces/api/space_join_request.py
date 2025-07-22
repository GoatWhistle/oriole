from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.spaces.schemas import SpaceJoinRequestUpdate
from features.spaces.services import space_join_request as service
from features.users.services.auth import get_current_active_auth_user_id
from shared.enums import SpaceJoinRequestStatusEnum
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.get(
    "/requests/{space_join_request_id}",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_space_join_request(
    space_join_request_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_space_join_request(session, user_id, space_join_request_id)
    return create_json_response(data=data)


@router.get(
    "/{space_id}/requests/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_space_join_requests_in_space(
    space_id: int,
    request: Request,
    status: SpaceJoinRequestStatusEnum | None = None,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_space_join_requests_in_space(
        session, user_id, space_id, status
    )
    base_url_with_query = request.url.include_query_params(
        status=status, page=page, per_page=per_page
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=str(base_url_with_query),
    )


@router.put(
    "/requests/{space_join_request_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def update_space_join_request(
    space_join_request_id: int,
    space_join_request_update: SpaceJoinRequestUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_space_join_request(
        session, user_id, space_join_request_id, space_join_request_update
    )
    return create_json_response(data=data)


@router.put(
    "/{space_id}/requests/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def update_space_join_requests_in_space(
    request: Request,
    space_id: int,
    space_join_request_update: SpaceJoinRequestUpdate,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_space_join_requests_in_space(
        session, user_id, space_id, space_join_request_update
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/{space_id}/requests/",
    )


@router.delete(
    "/requests/{space_join_request_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_space_join_request(
    space_join_request_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_space_join_request(session, user_id, space_join_request_id)


@router.delete(
    "/{space_id}/requests/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_space_join_requests_in_space(
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_space_join_requests_in_space(session, user_id, space_id)
