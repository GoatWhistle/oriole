from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect
from core.redis import redis_connection
from ..connections.manager import connection_manager
import json
from ..crud import message as crud
from features.groups.validators import get_account_or_404
from features.chat.crud.chat import get_chat_by_group_id
from ..repositories.messange_repo import MessageRepository


async def handle_websocket(
    websocket: WebSocket, group_id: int, user_id: int, session: AsyncSession
):
    account = await get_account_or_404(session, user_id, group_id)
    account_id = account.id

    await connection_manager.connect(
        websocket=websocket, group_id=group_id, account_id=account_id
    )
    await websocket.send_text(json.dumps({"type": "init", "account_id": account_id}))
    chat = await get_chat_by_group_id(session, group_id)
    chat_id = chat.id

    repo = MessageRepository(session)
    cache_key = f"chat:history:{group_id}"

    try:
        history = await crud.get_message_history(group_id, repo)
        await websocket.send_text(json.dumps({"type": "history", "messages": history}))

        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                continue

            if data.get("edit"):
                updated = await crud.update_message(
                    message_id=int(data.get("message_id")),
                    repo=repo,
                    new_text=data.get("message"),
                )
                if updated:
                    await redis_connection.redis.delete(cache_key)
                    await connection_manager.broadcast(
                        group_id,
                        json.dumps(
                            {
                                "edit": True,
                                "account_id": account_id,
                                "message": updated["message"],
                                "timestamp": updated["timestamp"],
                                "connectionId": data.get("connectionId"),
                                "message_id": updated["message_id"],
                                "is_edited": updated["is_edited"],
                            }
                        ),
                    )
                continue

            if data.get("delete"):
                deleted = await crud.delete_message(
                    message_id=int(data.get("message_id")),
                    repo=repo,
                    account_id=account_id,
                )
                if deleted:
                    await redis_connection.redis.delete(cache_key)
                    await connection_manager.broadcast(
                        group_id,
                        json.dumps(
                            {
                                "delete": True,
                                "message_id": data.get("message_id"),
                                "connectionId": data.get("connectionId"),
                            }
                        ),
                    )
                continue

            if data.get("message"):
                message_payload = await crud.save_new_message(
                    data=data,
                    group_id=group_id,
                    chat_id=chat_id,
                    account_id=account_id,
                    repo=repo,
                )
                await redis_connection.redis.delete(cache_key)
                await connection_manager.broadcast(
                    group_id, json.dumps(message_payload)
                )

    except WebSocketDisconnect:
        await connection_manager.disconnect(group_id, websocket)
