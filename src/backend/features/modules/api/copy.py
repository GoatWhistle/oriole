from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import ModuleRead
from features.modules.services import copy as service
from features.users.services.auth import get_current_active_auth_user_id
from utils import get_current_utc
from utils.schemas import SuccessResponse, Meta

router = APIRouter()


@router.post(
    "/{module_id}/copy-to-group/{target_group_id}",
    response_model=ModuleRead,
    status_code=status.HTTP_201_CREATED,
)
async def copy_module(
    module_id: int,
    target_group_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.copy_module_to_group(
        session, user_id, module_id, target_group_id
    )
    response_content = jsonable_encoder(
        SuccessResponse[ModuleRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)
