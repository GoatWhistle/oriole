from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

import features.solutions.services.code as solution_service
import features.tasks.services.code as task_service
import features.tasks.services.test as test_service
from database import db_helper
from features.solutions.schemas import CodeSolutionCreate
from features.tasks.schemas import (
    CodeTaskUpdate,
    CodeTaskCreate,
    TestUpdate,
    TestCreate,
)
from features.users.services.auth import get_current_active_auth_user_id
from utils.response_func import create_json_response
from utils.schemas import SuccessListResponse
from utils.schemas import SuccessResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.CREATED,
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
    status_code=HTTPStatus.OK,
)
async def update_code_task(
    task_update: CodeTaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await task_service.update_code_task(session, user_id, task_id, task_update)
    return create_json_response(data=data)


@router.post(
    "/tests",
    status_code=HTTPStatus.CREATED,
    response_model=SuccessResponse,
)
async def create_test(
    test_in: TestCreate,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.create_test(session, user_id, test_in)
    return create_json_response(data=data)


@router.get(
    "/tests/{test_id}",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_test_by_id(
    test_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.get_test_by_id(session, user_id, test_id)
    return create_json_response(data=data)


@router.get(
    "/{task_id}/tests/",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_tests_in_task(
    request: Request,
    task_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
    page: int | None = None,
    per_page: int | None = None,
):
    data = await test_service.get_tests_in_task(session, user_id, task_id)
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/tasks/code/{task_id}/tests/",
    )


@router.put(
    "/tests/{test_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def update_test(
    test_update: TestUpdate,
    test_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await test_service.update_test(session, user_id, test_id, test_update)
    return create_json_response(data=data)


@router.delete(
    "/tests/{test_id}/",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    await test_service.delete_test(session, user_id, test_id)


@router.post(
    "/{task_id}/solutions",
    status_code=HTTPStatus.OK,
    response_model=SuccessResponse,
)
async def create_code_solution(
    solution_in: CodeSolutionCreate,
    language: str,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.create_code_solution(
        session, user_id, solution_in, language
    )
    return create_json_response(data=data)


@router.post(
    "/{task_id}/solutions/upload",
    status_code=HTTPStatus.OK,
    response_model=SuccessResponse,
)
async def create_code_solution_file(
    task_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    code_text = (await file.read()).decode("utf-8")
    solution_in = CodeSolutionCreate(code=code_text, task_id=task_id)

    data = await solution_service.create_code_solution(session, user_id, solution_in)
    return create_json_response(data=data)


@router.get(
    "/{task_id}/solutions/{solution_id}/",
    response_model=SuccessResponse,
    status_code=HTTPStatus.OK,
)
async def get_code_solution_by_id(
    solution_id: int,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_code_solution_by_id(session, user_id, solution_id)
    return create_json_response(data=data)


@router.get(
    "/{task_id}/solutions",
    response_model=SuccessListResponse,
    status_code=HTTPStatus.OK,
)
async def get_user_solutions(
    request: Request,
    task_id: int,
    page: int | None = None,
    per_page: int | None = None,
    session: AsyncSession = Depends(db_helper.dependency_session_getter),
    user_id: int = Depends(get_current_active_auth_user_id),
):
    data = await solution_service.get_user_solutions_by_task_id(
        session, user_id, task_id
    )
    return create_json_response(
        data=data,
        page=page,
        per_page=per_page,
        base_url=f"{str(request.base_url).rstrip("/")}/api/solution/code/",
    )
