from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.notifications.models.notification_settings import UserNotificationSettings
from features.notifications.schemas.notification_settings import (
    UserNotificationSettingsUpdate,
)
from features.notifications.services.notification_settings import (
    update_notification_settings,
)
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter(tags=["Notifications"])


@router.put("/notification-settings", response_model=UserNotificationSettings)
async def update_user_notification_settings(
    settings_update: UserNotificationSettingsUpdate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    try:
        return await update_notification_settings(
            session=session, user_id=user_id, settings_update=settings_update
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
