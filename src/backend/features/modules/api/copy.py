from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.services import copy as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/{module_id}/copy-to-group/{target_group_id}",
    response_model=SuccessResponse,
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
    return create_json_response(data=data)
