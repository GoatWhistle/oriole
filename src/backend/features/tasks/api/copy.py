from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.schemas import TaskRead
from features.tasks.services import copy as service
from features.users.services.auth import get_current_active_auth_user_id
from utils import get_current_utc
from utils.schemas import SuccessResponse, Meta

router = APIRouter()


@router.post(
    "/{task_id}/copy-to-module/{target_module_id}",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def copy_task_to_module(
    source_task_id: int,
    target_module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.copy_task_to_module(
        session, user_id, source_task_id, target_module_id
    )
    response_content = jsonable_encoder(
        SuccessResponse[TaskRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)
