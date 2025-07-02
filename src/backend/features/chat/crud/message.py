from datetime import datetime, timezone

import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.redis import redis_connection
from src.backend.features.chat.models.message import Message


async def update_message(
    user_id: int,
    message_id: int,
    session: AsyncSession,
    new_text: str,
):
    try:
        message_id = int(message_id)
    except (ValueError, TypeError):
        return None

    message = await session.get(Message, message_id)
    if message and message.sender_id == user_id:
        message.text = new_text
        await session.commit()
        return message
    return None


async def delete_message(
    user_id: int,
    message_id: int,
    session: AsyncSession,
):
    try:
        message_id = int(message_id)
    except (ValueError, TypeError):
        return None

    message = await session.get(Message, message_id)
    if message and message.sender_id == user_id:
        await session.delete(message)
        await session.commit()
        return message
    return None

async def get_message_history(group_id: int, session: AsyncSession):
    cache_key = f"chat:history:{group_id}"
    cached = await redis_connection.redis.get(cache_key)

    if cached:
        return json.loads(cached)

    stmt = (
        select(Message)
        .where(Message.group_id == group_id)
        .order_by(Message.timestamp)
    )
    result = await session.execute(stmt)
    messages = result.scalars().all()
    msg_dict = {msg.id: msg for msg in messages}

    history = [
        {
            "user_id": msg.sender_id,
            "message": msg.text,
            "timestamp": msg.timestamp.isoformat(),
            "message_id": msg.id,
            "reply_to": msg.reply_to,
            "reply_to_text": msg_dict[msg.reply_to].text if msg.reply_to in msg_dict else None,
        }
        for msg in messages
    ]

    await redis_connection.redis.setex(cache_key, 600, json.dumps(history))
    return history


async def save_new_message(data, group_id: int, user_id: int, session: AsyncSession):
    timestamp = datetime.now(timezone.utc)
    try:
        reply_to = int(data.get("reply_to"))
    except (ValueError, TypeError):
        reply_to = None

    message = Message(
        text=data.get("message", ""),
        group_id=group_id,
        sender_id=user_id,
        timestamp=timestamp,
        reply_to=reply_to,
    )
    session.add(message)
    await session.commit()

    return {
        "user_id": user_id,
        "message": message.text,
        "timestamp": timestamp.isoformat(),
        "connectionId": data.get("connectionId"),
        "message_id": message.id,
        "reply_to": reply_to,
        "reply_to_text": data.get("reply_to_text"),
    }

