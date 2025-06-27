from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import (
    ModuleCreate,
    ModuleUpdate,
    ModuleUpdatePartial,
)
from features.modules.services import module as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse, SuccessListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    module_in: ModuleCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_module(session, user_id, module_in)
    return create_json_response(data=data)


@router.get(
    "/{module_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_module_by_id(
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    include: list[str] | None = Query(None),
):
    data = await service.get_module_by_id(session, user_id, module_id, include)
    return create_json_response(data=data)


@router.get(
    "/",
    response_model=list[SuccessListResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_modules(
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    page: int | None = None,
    per_page: int | None = None,
    include: list[str] | None = Query(None),
):
    data = await service.get_user_modules(
        session=session, user_id=user_id, is_active=is_active, include=include
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"http://127.0.0.1:8000/api/modules/?is_active={is_active if is_active else False}",
        include=include,
    )


@router.put(
    "/{module_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_module(
    module_update: ModuleUpdate,
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_module(
        session, user_id, module_id, module_update, False
    )
    return create_json_response(data=data)


@router.patch(
    "/{module_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_module_partial(
    module_update: ModuleUpdatePartial,
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_module(session, user_id, module_id, module_update, True)
    return create_json_response(data=data)


@router.delete(
    "/{module_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_module(
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await service.delete_module(session, user_id, module_id)
