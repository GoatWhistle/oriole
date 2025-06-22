from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from features.modules.schemas import (
    ModuleCreate,
    ModuleUpdate,
    ModuleUpdatePartial,
    ModuleRead,
)
from features.modules.services import module as service
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_list_response
from utils.schemas import SuccessResponse, Meta, SuccessListResponse
from utils.time_manager import get_current_utc

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse[ModuleRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    module_in: ModuleCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.create_module(session, user_id, module_in)
    response_content = jsonable_encoder(
        SuccessResponse[ModuleRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=201)


@router.get(
    "/{module_id}/",
    response_model=SuccessResponse[ModuleRead],
    status_code=status.HTTP_200_OK,
)
async def get_module_by_id(
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.get_module_by_id(session, user_id, module_id)
    response_content = jsonable_encoder(
        SuccessResponse[ModuleRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.get(
    "/",
    response_model=list[SuccessListResponse[ModuleRead]],
    status_code=status.HTTP_200_OK,
)
async def get_user_modules(
    is_active: bool | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    page: int | None = None,
    per_page: int | None = None,
):
    data = await service.get_user_modules(session, user_id, is_active)
    response_content = create_list_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"http://127.0.0.1:8000/api/modules/?is_active={is_active}",
    )
    return JSONResponse(content=response_content, status_code=200)


@router.put(
    "/{module_id}/",
    response_model=SuccessResponse[ModuleRead],
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
    response_content = jsonable_encoder(
        SuccessResponse[ModuleRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


@router.patch(
    "/{module_id}/",
    response_model=SuccessResponse[ModuleRead],
    status_code=status.HTTP_200_OK,
)
async def update_module_partial(
    module_update: ModuleUpdatePartial,
    module_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await service.update_module(session, user_id, module_id, module_update, True)
    response_content = jsonable_encoder(
        SuccessResponse[ModuleRead](
            data=data, meta=Meta(version="v1", timestamp=str(get_current_utc()))
        )
    )
    return JSONResponse(content=response_content, status_code=200)


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
