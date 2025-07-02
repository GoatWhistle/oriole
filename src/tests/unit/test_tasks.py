import pytest

from src.backend.features.tasks.mappers.task import (
    build_task_read,
    build_task_read_list,
)
from src.backend.features.tasks.services.string_match import (
    create_string_match_task,
    get_task_by_id,
    get_tasks_in_module,
    get_user_tasks,
    update_task,
)


# Mappers
def test_build_task_read_without_user_reply(sample_task, sample_module):
    result = build_task_read(task=sample_task, module=sample_module)

    assert result.id == sample_task.id
    assert result.title == sample_task.title
    assert result.is_correct is False
    assert not hasattr(result, "user_answer")
    assert not hasattr(result, "user_attempts")


def test_build_task_read_with_user_reply(sample_task, sample_module, sample_user_reply):
    result = build_task_read(
        task=sample_task,
        module=sample_module,
        user_reply=sample_user_reply,
    )

    assert result.is_correct == sample_user_reply.is_correct
    assert result.user_answer == sample_user_reply.user_answer
    assert result.user_attempts > 0


def test_build_task_read_list(sample_task, sample_module, sample_user_reply):
    result = build_task_read_list(
        tasks=[sample_task], modules=[sample_module], user_replies=[sample_user_reply]
    )
    assert result[0].is_correct == sample_user_reply.is_correct
    assert result[0].user_answer == sample_user_reply.user_answer
    assert result[0].user_attempts > 0


def test_build_task_read_list_task_without_module(sample_task, sample_module):
    result = build_task_read_list([], [sample_task], [])
    assert len(result) == 0


# Services
@pytest.mark.asyncio
async def test_create_task_success(
    mock_session,
    valid_task_data,
    mock_get_module_or_404,
    mock_get_account_or_404,
    mock_task_crud_create_task,
):
    result = await create_string_match_task(
        session=mock_session, user_id=1, task_in=valid_task_data
    )

    assert result.id == 1
    assert result.title == valid_task_data.title
    assert result.module_id == valid_task_data.module_id


@pytest.mark.asyncio
async def test_get_task_by_id(
    mock_session,
    mock_get_module_or_404,
    mock_get_task_or_404,
    mock_get_account_or_404,
    mock_get_user_reply_by_account_id_and_task_id,
    mock_task,
    mock_module,
):
    user_id = 1
    result = await get_task_by_id(
        session=mock_session, user_id=user_id, task_id=mock_task.id
    )

    assert result.id == mock_task.id
    assert result.title == mock_task.title
    assert result.module_id == mock_module.id


@pytest.mark.asyncio
async def test_get_tasks_in_module(
    mock_session,
    mock_get_module_or_404,
    mock_get_account_or_404,
    mock_task_crud_get_tasks_by_module_id,
    mock_get_user_replies_by_account_ids_and_task_ids,
    mock_task,
    mock_module,
):
    user_id = 1
    result = await get_tasks_in_module(
        session=mock_session,
        user_id=user_id,
        module_id=mock_module.id,
        is_active=False,
    )
    assert result[0].id == mock_task.id
    assert result[0].title == mock_task.title
    assert result[0].module_id == mock_module.id


@pytest.mark.asyncio
async def test_get_user_tasks(
    mock_session,
    mock_account_crud_get_accounts_by_user_id,
    mock_module_crud_get_modules_by_group_ids,
    mock_task_crud_get_tasks_by_module_ids,
    mock_get_user_replies_by_account_ids_and_task_ids,
    mock_task,
    mock_module,
):
    user_id = 1
    result = await get_user_tasks(
        session=mock_session,
        user_id=user_id,
        is_active=False,
    )

    assert result[0].id == mock_task.id
    assert result[0].title == mock_task.title
    assert result[0].module_id == mock_module.id


@pytest.mark.asyncio
async def test_update_task(
    mock_session,
    valid_task_data,
    mock_get_module_or_404,
    mock_get_task_or_404,
    mock_get_account_or_404,
    mock_get_user_reply_by_account_id_and_task_id,
    mock_task,
    mock_module,
):
    user_id = 1
    result = await update_task(
        session=mock_session,
        user_id=user_id,
        task_id=mock_task.id,
        task_update=valid_task_data,
        is_partial=False,
    )

    assert result.id == mock_task.id
    assert result.title == mock_task.title
    assert result.module_id == mock_module.id
