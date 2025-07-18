from http import HTTPStatus

from fastapi import APIRouter, Depends
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
async def get_space_join_request_by_id(
    space_join_request_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_space_join_request_by_id(
        session, user_id, space_join_request_id
    )
    return create_json_response(data=data)


@router.get(
    "/{space_id}/requests/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_space_join_requests_by_space_id(
    space_id: int,
    status: SpaceJoinRequestStatusEnum | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_space_join_requests_by_space_id(
        session, user_id, space_id, status
    )
    return create_json_response(data=data)


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
async def update_space_join_requests_by_space_id(
    space_join_request_id: int,
    space_join_request_update: SpaceJoinRequestUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_space_join_requests_by_space_id(
        session, user_id, space_join_request_id, space_join_request_update
    )
    return create_json_response(data=data)


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
async def delete_space_join_requests_by_space_id(
    space_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
) -> None:
    await service.delete_space_join_requests_by_space_id(session, user_id, space_id)
