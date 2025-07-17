from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from shared.enums import NotificationTypeEnum


class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: NotificationTypeEnum
    related_entity_id: Optional[int] = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationRead(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True