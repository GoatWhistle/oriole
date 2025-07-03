from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.services.code as task_service
import features.tasks.services.test as test_service
from database import db_helper
from features.tasks.schemas import (
    CodeTaskUpdate,
    CodeTaskUpdatePartial,
    CodeTaskCreate,
    TestUpdate,
    TestUpdatePartial,
    TestCreate,
)
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_code_task(
    task_in: CodeTaskCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.create_code_task(session, user_id, task_in)
    return create_json_response(data=data)


@router.put(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_code_task(
    task_update: CodeTaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.update_code_task(
        session, user_id, task_id, task_update, False
    )
    return create_json_response(data=data)


@router.patch(
    "/{task_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_code_task_partial(
    task_update: CodeTaskUpdatePartial,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.update_code_task(
        session, user_id, task_id, task_update, True
    )
    return create_json_response(data=data)


@router.post(
    "/test", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse
)
async def create_test(
    test_in: TestCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.create_test(session, user_id, test_in)
    return create_json_response(data=data)


@router.put(
    "/test/{test_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_test(
    test_update: TestUpdate,
    test_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.update_test(session, user_id, test_id, test_update, False)
    return create_json_response(data=data)


@router.patch(
    "/test/{test_id}/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def update_test_partial(
    test_update: TestUpdatePartial,
    test_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.update_test(session, user_id, test_id, test_update, True)
    return create_json_response(data=data)
