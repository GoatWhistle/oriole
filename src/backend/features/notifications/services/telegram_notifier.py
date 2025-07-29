import requests

from core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession
from features.users.crud.user import get_user_by_id

BASE_URL = f"https://api.telegram.org/bot{settings.telegram.bot_token}"


async def send_personal_notification(
    cls,
    session: AsyncSession,
    user_id: int,
    title: str,
    message: str,
    notification_type: str,
    entity_id: int | None = None,
):
    user = await get_user_by_id(session=session, user_id=user_id)
    if not user or not user.telegram_id:
        return False

    text = f"🔔 *{title}*\n\n{message}"
    if entity_id:
        text += f"\n\nID объекта: {entity_id}"

    payload = {"chat_id": user.telegram_id, "text": text, "parse_mode": "Markdown"}

    try:
        response = requests.post(f"{cls.BASE_URL}/sendMessage", json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram sending error: {e}")
        return False
