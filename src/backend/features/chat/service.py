from starlette.websockets import WebSocket, WebSocketDisconnect
from .manager import connection_manager
import json

async def handle_websocket(websocket: WebSocket, group_id: int, user_id: int):
    await connection_manager.connect(websocket, group_id, user_id)

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
                msg = {
                    "user_id": data.get("user_id", user_id),
                    "message": data.get("message", ""),
                    "connectionId": data.get("connectionId", None)
                }
                await connection_manager.broadcast(group_id, json.dumps(msg))
            except json.JSONDecodeError:
                print("[websocket] ❌ Invalid JSON")
    except WebSocketDisconnect:
        await connection_manager.disconnect(group_id, websocket)
