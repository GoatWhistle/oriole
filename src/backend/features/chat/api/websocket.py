from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from database import db_helper
from ..services import chat as service

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    group_id: int,
    user_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
):
    return await service.handle_websocket(
        websocket=websocket,
        group_id=group_id,
        user_id=user_id,
        session=session,
    )
