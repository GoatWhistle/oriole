from datetime import datetime, timezone
import json


from core.redis import redis_connection
from ..exeptions import InvalidMessageIdException, MessageNotFoundOrForbiddenException
from ..models.message import Message
from ..repositories.messange_repo import MessageRepository


async def save_new_message(
    data, group_id: int, chat_id: int, account_id: int, repo: MessageRepository
):

    timestamp = datetime.now(timezone.utc)
    try:
        reply_to = int(data.get("reply_to"))
    except (ValueError, TypeError):
        reply_to = None

    message = Message(
        text=data.get("message", ""),
        group_id=group_id,
        chat_id=chat_id,
        account_id=account_id,
        timestamp=timestamp,
        reply_to=reply_to,
    )

    await repo.save_new_message(message)

    return {
        "user_id": account_id,
        "message": message.text,
        "timestamp": timestamp.isoformat(),
        "connectionId": data.get("connectionId"),
        "message_id": message.id,
        "reply_to": reply_to,
        "reply_to_text": data.get("reply_to_text"),
    }


async def get_message_history(group_id: int, repo: MessageRepository):

    cache_key = f"chat:history:{group_id}"
    cached = await redis_connection.redis.get(cache_key)

    if cached:
        return json.loads(cached)

    messages = await repo.get_messages_by_group(group_id)
    msg_dict = {msg.id: msg for msg in messages}

    history = [
        {
            "user_id": msg.account_id,
            "message": msg.text,
            "timestamp": msg.timestamp.isoformat(),
            "message_id": msg.id,
            "reply_to": msg.reply_to,
            "reply_to_text": (
                msg_dict[msg.reply_to].text if msg.reply_to in msg_dict else None
            ),
        }
        for msg in messages
    ]

    await redis_connection.redis.setex(cache_key, 600, json.dumps(history))
    return history


async def delete_message(
    account_id: int,
    message_id: int,
    repo: MessageRepository,
):

    try:
        message_id = int(message_id)
    except (ValueError, TypeError):
        raise InvalidMessageIdException(message_id)

    message = await repo.get_by_id(message_id)
    if not message or message.account_id != account_id:
        raise MessageNotFoundOrForbiddenException(message_id)

    await repo.delete(message)
    return message


async def update_message(
    account_id: int,
    message_id: int,
    new_text: str,
    repo: MessageRepository,
):

    try:
        message_id = int(message_id)
    except (ValueError, TypeError):
        raise InvalidMessageIdException(message_id)

    message = await repo.get_by_id(message_id)
    if not message or message.account_id != account_id:
        raise MessageNotFoundOrForbiddenException(message_id)

    await repo.update_message(message, new_text)
    return message
