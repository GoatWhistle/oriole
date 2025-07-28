from pydantic import BaseModel

class UserNotificationSettingsUpdate(BaseModel):
    email_enabled: bool
    telegram_enabled: bool

    chat_notifications_enabled: bool
    system_notifications_enabled: bool
    deadline_notifications_enabled: bool