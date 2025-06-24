from typing import List, Dict

from starlette.websockets import WebSocket

"""        {group_id1:[ (websocket1,user_id1),
                     (websocket2,user_id1)
                     ...
                     ],
         group_id2 : [(websocket1,user_id1),
                     (websocket2,user_id1)
                     ...
                      ]
         }"""


class ConnectionManager:
    def __init__(self):
        self.group_connections: Dict[int, List[tuple[WebSocket, int]]] = dict()

    async def connect(self, websocket: WebSocket, group_id: int, user_id: int):
        await websocket.accept()
        self.group_connections.setdefault(group_id, []).append((websocket, user_id))

    async def disconnect(self, group_id: int, websocket: WebSocket):
        await websocket.close()
        conns = self.group_connections.get(group_id, [])
        self.group_connections[group_id] = [(ws, uid) for ws, uid in conns if ws != websocket]

    async def broadcast(self, group_id: int, websocket: WebSocket, message: str):
        for ws, uid in self.group_connections.get(group_id, []):
            await ws.send_text(message)

    def get_connected_user_ids(self, group_id: int) -> List[int]:
        return [uid for _, uid in self.group_connections.get(group_id, [])]

