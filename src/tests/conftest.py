from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from features.groups.schemas import AccountRole
from features.tasks.schemas import TaskCreate


@pytest.fixture
def sample_task():
    task = MagicMock(
        spec=[
            "id",
            "title",
            "description",
            "start_datetime",
            "end_datetime",
            "max_attempts",
            "is_active",
            "module_id",
        ]
    )
    task.id = 1
    task.title = "Test Task"
    task.description = "Test Description"
    task.start_datetime = datetime(2023, 1, 1)
    task.end_datetime = datetime(2023, 12, 31)
    task.max_attempts = 3
    task.is_active = True
    task.module_id = 1
    return task


@pytest.fixture
def sample_module():
    module = MagicMock(spec=["id", "title", "group_id"])
    module.id = 1
    module.title = "Test Module"
    module.group_id = 1
    return module


@pytest.fixture
def sample_user_reply():
    reply = MagicMock(
        spec=["id", "user_answer", "is_correct", "user_attempts", "task_id", "user_id"]
    )
    reply.id = 1
    reply.user_answer = "Test Answer"
    reply.is_correct = True
    reply.user_attempts = 2
    reply.task_id = 1
    reply.user_id = 1
    return reply


# @pytest.fixture
# def mock_session():
#     session = AsyncMock()
#     session.commit = AsyncMock()
#     return session


@pytest.fixture
def mock_crud():
    crud = MagicMock()
    crud.create_task = AsyncMock(return_value=MagicMock(id=1))
    crud.increment_module_tasks_count = AsyncMock()
    return crud


@pytest.fixture
def now():
    return datetime.now(timezone.utc)


@pytest.fixture
def mock_task(now):
    task = MagicMock()
    task.id = 1
    task.title = "Test Task"
    task.description = "Test Description"
    task.correct_answer = "aboba"
    task.start_datetime = now + timedelta(days=1)
    task.end_datetime = now + timedelta(days=2)
    task.max_attempts = 3
    task.is_active = True
    task.module_id = 1
    return task


@pytest.fixture
def mock_module(now):
    module = MagicMock()
    module.id = 1
    module.group_id = 1
    module.start_datetime = now - timedelta(days=1)
    module.end_datetime = now + timedelta(days=4)
    module.title = "Test Module"
    module.description = "Module Description"
    module.is_contest = True
    module.admin_id = 1
    module.tasks_count = 1
    module.is_active = False
    return module


@pytest.fixture
def mock_account():
    account = MagicMock()
    account.role = AccountRole.ADMIN
    account.id = 1
    account.group_id = 1
    return account


@pytest.fixture
def mock_reply():
    reply = MagicMock()
    reply.id = 1
    reply.account_id = 2
    reply.task_id = 1
    reply.user_answer = "aboba"
    reply.is_correct = False
    reply.user_attempts = 5
    return reply


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def valid_task_data(now):
    return TaskCreate(
        title="Test Task",
        description="Test Description",
        start_datetime=now + timedelta(days=1),
        end_datetime=now + timedelta(days=2),
        max_attempts=3,
        module_id=1,
        correct_answer="baza",
    )


@pytest.fixture
def mock_get_task_or_404(mock_task):
    with patch(
        "src.backend.features.tasks.services.task.get_task_or_404",
        AsyncMock(return_value=mock_task),
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_module_or_404(mock_module):
    with patch(
        "src.backend.features.tasks.services.task.get_module_or_404",
        AsyncMock(return_value=mock_module),
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_account_or_404(mock_account):
    with patch(
        "src.backend.features.tasks.services.task.get_account_or_404",
        AsyncMock(return_value=mock_account),
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_user_reply_by_account_id_and_task_id(mock_reply):
    with patch(
        "src.backend.features.tasks.services.task.user_reply_crud.get_user_reply_by_account_id_and_task_id",
        AsyncMock(return_value=mock_reply),
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_user_replies_by_account_ids_and_task_ids(mock_reply):
    with patch(
        "src.backend.features.tasks.services.task.user_reply_crud.get_user_replies_by_account_ids_and_task_ids",
        AsyncMock(return_value=mock_reply),
    ) as mock:
        yield mock


@pytest.fixture
def mock_task_crud_create_task(mock_task):
    with patch(
        "src.backend.features.tasks.services.task.task_crud.create_task",
        AsyncMock(return_value=mock_task),
    ) as mock:
        yield mock


@pytest.fixture
def mock_task_crud_get_tasks_by_module_id(mock_task):
    with patch(
        "src.backend.features.tasks.services.task.task_crud.get_tasks_by_module_id",
        AsyncMock(return_value=[mock_task]),
    ) as mock:
        yield mock


@pytest.fixture
def mock_task_crud_get_tasks_by_module_ids(mock_task):
    with patch(
        "src.backend.features.tasks.services.task.task_crud.get_tasks_by_module_ids",
        AsyncMock(return_value=[mock_task]),
    ) as mock:
        yield mock


@pytest.fixture
def mock_account_crud_get_accounts_by_user_id(mock_account):
    with patch(
        "src.backend.features.tasks.services.task.account_crud.get_accounts_by_user_id",
        AsyncMock(return_value=[mock_account]),
    ) as mock:
        yield mock


@pytest.fixture
def mock_module_crud_get_modules_by_group_ids(mock_account):
    with patch(
        "src.backend.features.tasks.services.task.module_crud.get_modules_by_group_ids",
        AsyncMock(return_value=[mock_account]),
    ) as mock:
        yield mock
