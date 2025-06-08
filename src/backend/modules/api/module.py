from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from modules.schemas import (
    ModuleCreate,
    ModuleRead,
    ModuleReadPartial,
    ModuleUpdate,
    ModuleUpdatePartial,
)
from modules.services import module as service
from users.services.auth import get_current_active_auth_user_id

router = APIRouter()


@router.post(
    "/",
    response_model=ModuleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_in: ModuleCreate,
):
    return await service.create_module(
        session=session,
        user_id=user_id,
        module_in=module_in,
    )


@router.get(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def get_module_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_id: int,
):
    return await service.get_module_by_id(
        session=session,
        user_id=user_id,
        module_id=module_id,
    )


@router.get(
    "/",
    response_model=Sequence[ModuleReadPartial],
    status_code=status.HTTP_200_OK,
)
async def get_user_modules(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
):
    return await service.get_user_modules(
        session=session,
        user_id=user_id,
    )


@router.put(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def update_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_update: ModuleUpdate,
    module_id: int,
):
    return await service.update_module(
        session=session,
        user_id=user_id,
        module_id=module_id,
        module_update=module_update,
        is_partial=False,
    )


@router.patch(
    "/{module_id}/",
    response_model=ModuleRead,
    status_code=status.HTTP_200_OK,
)
async def update_module_partial(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_update: ModuleUpdatePartial,
    module_id: int,
):
    return await service.update_module(
        session=session,
        user_id=user_id,
        module_id=module_id,
        module_update=module_update,
        is_partial=True,
    )


@router.delete(
    "/{module_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_module(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.dependency_session_getter),
    ],
    user_id: Annotated[
        int,
        Depends(get_current_active_auth_user_id),
    ],
    module_id: int,
) -> None:
    await service.delete_module(
        session=session,
        user_id=user_id,
        module_id=module_id,
    )




