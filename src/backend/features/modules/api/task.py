from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.tasks.services import base as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessListResponse

router = APIRouter()


@router.get(
    "/{module_id}/tasks/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_tasks_in_module(
    request: Request,
    module_id: int,
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    per_page: int | None = None,
    page: int | None = None,
):
    data = await service.get_tasks_in_module(session, user_id, module_id, is_active)
    base_url_with_query = request.url.include_query_params(
        is_active=is_active, page=page, per_page=per_page
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=str(base_url_with_query),
    )
