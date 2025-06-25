from fastapi import APIRouter
from starlette.websockets import WebSocket
from . import service
router = APIRouter()

@router.websocket("/")
async def websocket_endpoint(
        websocket: WebSocket,
        group_id : int,
        user_id : int,
):
    return await service.handle_websocket(
        websocket=websocket,
        group_id=group_id,
        user_id=user_id,
    )