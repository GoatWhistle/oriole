from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.notifications.services import notification as notification_service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter(tags=["Notifications"], prefix="/notifications")


@router.get(
    "/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_user_notifications(
    request: Request,
    unread_only: bool = False,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await notification_service.get_user_notifications(
        session, user_id, unread_only=unread_only
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip('/')}/api/notifications/?unread_only={unread_only}",
    )


@router.get(
    "/{notification_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_notification_by_id(
    notification_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await notification_service.get_notification_by_id(
        session, user_id, notification_id
    )
    return create_json_response(data=data)


@router.post(
    "/{notification_id}/read/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def mark_as_read(
    notification_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await notification_service.mark_notification_as_read(
        session, user_id, notification_id
    )


@router.post(
    "/read-all/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def mark_all_as_read(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await notification_service.mark_all_as_read(session, user_id)


@router.get(
    "/unread-count/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_unread_count(
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    count = await notification_service.get_unread_notifications_count(session, user_id)
    return create_json_response(data={"count": count})


@router.delete(
    "/{notification_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_notification(
    notification_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await notification_service.delete_notification(session, user_id, notification_id)
