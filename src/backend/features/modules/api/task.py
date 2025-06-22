from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.schemas import TaskRead
from features.tasks.services import task as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_list_response
from utils.schemas import SuccessListResponse

router = APIRouter()


@router.get(
    "/{module_id}/tasks/",
    response_model=SuccessListResponse[TaskRead],
    status_code=status.HTTP_200_OK,
)
async def get_tasks_in_module(
    module_id: int,
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    per_page: int | None = None,
    page: int | None = None,
):
    data = await service.get_tasks_in_module(session, user_id, module_id, is_active)
    response_content = create_list_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"http://127.0.0.1:8000/api/modules/{module_id}/tasks/?is_active={is_active if is_active else False}",
    )
    return JSONResponse(content=response_content, status_code=200)
