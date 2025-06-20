from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import (
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
    ModuleUpdatePartial,
)
from features.modules.services import module as service
from features.users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.post(
    "/",
    response_model=ModuleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    module_in: ModuleCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.create_module(session, user_id, module_in)


@router.get(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def get_module_by_id(
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.get_module_by_id(session, user_id, module_id)


@router.get(
    "/",
    response_model=list[ModuleRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_modules(
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.get_user_modules(session, user_id, is_active)


@router.put(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def update_module(
    module_update: ModuleUpdate,
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.update_module(
        session, user_id, module_id, module_update, False
    )


@router.patch(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def update_module_partial(
    module_update: ModuleUpdatePartial,
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    return await service.update_module(session, user_id, module_id, module_update, True)


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
