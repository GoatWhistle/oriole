from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.redis import redis_connection
from .manager import connection_manager
from .models import Message
import json


async def handle_websocket(
    websocket: WebSocket, group_id: int, user_id: int, session: AsyncSession
):
    await connection_manager.connect(websocket, group_id, user_id)

    cache_key = f"chat:history:{group_id}"

    try:
        cached_history = None
        try:
            cached_history = await redis_connection.redis.get(cache_key)
        except Exception as e:
            print(f"Redis get error: {e}")

        if cached_history:
            history_payload = json.loads(cached_history)
        else:
            history_stmt = (
                select(Message)
                .where(Message.group_id == group_id)
                .order_by(Message.timestamp)
            )
            result = await session.execute(history_stmt)
            messages = result.scalars().all()
            msg_dict = {msg.id: msg for msg in messages}

            history_payload = [
                {
                    "user_id": msg.sender_id,
                    "message": msg.text,
                    "timestamp": msg.timestamp.isoformat(),
                    "message_id": msg.id,
                    "reply_to": msg.reply_to,
                    "reply_to_text": (
                        msg_dict[msg.reply_to].text
                        if msg.reply_to in msg_dict
                        else None
                    ),
                }
                for msg in messages
            ]

            try:
                await redis_connection.redis.setex(
                    cache_key, 600, json.dumps(history_payload)
                )
            except Exception as e:
                print(f"Redis setex error: {e}")

        await websocket.send_text(
            json.dumps({"type": "history", "messages": history_payload})
        )

        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)

                if data.get("edit"):
                    new_text = data.get("message")
                    message_id = data.get("message_id")

                    updated_message = await update_message(
                        user_id=user_id,
                        new_text=new_text,
                        session=session,
                        message_id=message_id,
                    )
                    if updated_message:
                        upd_msg = {
                            "edit": True,
                            "user_id": user_id,
                            "message": new_text,
                            "timestamp": updated_message.timestamp.isoformat(),
                            "connectionId": data.get("connectionId"),
                            "message_id": message_id,
                        }
                        try:
                            await redis_connection.redis.delete(cache_key)
                        except Exception as e:
                            print(f"Redis delete error: {e}")

                        await connection_manager.broadcast(
                            group_id=group_id, message=json.dumps(upd_msg)
                        )
                    continue

                if data.get("delete"):
                    deleted_message_id = data.get("message_id")

                    deleted = await delete_message(
                        message_id=deleted_message_id,
                        session=session,
                        user_id=user_id,
                    )
                    if deleted:
                        del_msg = {
                            "delete": True,
                            "message_id": deleted_message_id,
                            "connectionId": data.get("connectionId"),
                        }
                        try:
                            await redis_connection.redis.delete(cache_key)
                        except Exception as e:
                            print(f"Redis delete error: {e}")

                        await connection_manager.broadcast(
                            group_id=group_id, message=json.dumps(del_msg)
                        )
                    continue

                text = data.get("message", "")
                if not text:
                    continue

                timestamp = datetime.now(timezone.utc)

                # Обработка reply_to
                try:
                    reply_to = int(data.get("reply_to"))
                except (ValueError, TypeError):
                    reply_to = None

                reply_to_text = data.get("reply_to_text")

                message = Message(
                    text=text,
                    group_id=group_id,
                    sender_id=user_id,
                    timestamp=timestamp,
                    reply_to=reply_to,
                )

                session.add(message)
                await session.commit()

                msg = {
                    "user_id": user_id,
                    "message": text,
                    "timestamp": timestamp.isoformat(),
                    "connectionId": data.get("connectionId"),
                    "message_id": message.id,
                    "reply_to": reply_to,
                    "reply_to_text": reply_to_text,
                }

                try:
                    await redis_connection.redis.delete(cache_key)
                except Exception as e:
                    print(f"Redis delete error: {e}")

                await connection_manager.broadcast(group_id, json.dumps(msg))

            except json.JSONDecodeError:
                print("[websocket] Invalid JSON")

    except WebSocketDisconnect:
        await connection_manager.disconnect(group_id, websocket)


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
