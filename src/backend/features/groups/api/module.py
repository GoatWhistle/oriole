from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import ModuleRead
from features.modules.services import module as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response

router = APIRouter()


@router.get(
    "/{group_id}/modules/",
    response_model=list[ModuleRead],
    status_code=status.HTTP_200_OK,
)
async def get_modules_in_group(
    group_id: int,
    request: Request,
    page: int | None = None,
    per_page: int | None = None,
    is_active: bool | None = None,
    include: list[str] | None = Query(None),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_modules_in_group(
        session=session,
        user_id=user_id,
        group_id=group_id,
        is_active=is_active,
        include=include,
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/groups/{group_id}/modules/?is_active={is_active if is_active else False}",
        include=include,
    )
