from typing import List, Dict
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.group_connections: Dict[int, List[tuple[WebSocket, int]]] = {}

    async def connect(self, websocket: WebSocket, group_id: int, account_id: int):
        await websocket.accept()
        self.group_connections.setdefault(group_id, []).append((websocket, account_id))

    async def disconnect(self, group_id: int, websocket: WebSocket):
        conns = self.group_connections.get(group_id, [])
        self.group_connections[group_id] = [
            (ws, uid) for ws, uid in conns if ws != websocket
        ]

    async def broadcast(self, group_id: int, message: str):
        for ws, _ in self.group_connections.get(group_id, []):
            await ws.send_text(message)

    def get_connected_user_ids(self, group_id: int) -> List[int]:
        return [uid for _, uid in self.group_connections.get(group_id, [])]


connection_manager = ConnectionManager()
