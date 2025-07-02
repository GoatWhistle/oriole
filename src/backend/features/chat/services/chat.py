from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect
from src.backend.core.redis import redis_connection
from src.backend.features.chat.connections.manager import connection_manager
import json
from ..crud import message as crud


async def handle_websocket(websocket: WebSocket, group_id: int, user_id: int, session: AsyncSession):
    await connection_manager.connect(websocket, group_id, user_id)
    cache_key = f"chat:history:{group_id}"

    try:
        history = await crud.get_message_history(group_id, session)
        await websocket.send_text(json.dumps({"type": "history", "messages": history}))

        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                print("[websocket] Invalid JSON")
                continue

            if data.get("edit"):
                updated = await crud.update_message(
                    user_id, data.get("message"), session, data.get("message_id")
                )
                if updated:
                    await redis_connection.redis.delete(cache_key)
                    await connection_manager.broadcast(group_id, json.dumps({
                        "edit": True,
                        "user_id": user_id,
                        "message": data.get("message"),
                        "timestamp": updated.timestamp.isoformat(),
                        "connectionId": data.get("connectionId"),
                        "message_id": data.get("message_id"),
                    }))
                continue

            if data.get("delete"):
                deleted = await crud.delete_message(
                    message_id=data.get("message_id"), session=session, user_id=user_id
                )
                if deleted:
                    await redis_connection.redis.delete(cache_key)
                    await connection_manager.broadcast(group_id, json.dumps({
                        "delete": True,
                        "message_id": data.get("message_id"),
                        "connectionId": data.get("connectionId"),
                    }))
                continue

            if data.get("message"):
                message_payload = await crud.save_new_message(data, group_id, user_id, session)
                await redis_connection.redis.delete(cache_key)
                await connection_manager.broadcast(group_id, json.dumps(message_payload))

    except WebSocketDisconnect:
        await connection_manager.disconnect(group_id, websocket)
