from sqlalchemy.ext.asyncio import AsyncSession

import features.tasks.crud.test as test_crud
import features.tasks.mappers as mapper
from features.groups.validators import (
    get_account_or_404,
    check_user_is_admin_or_owner,
)
from features.modules.validators import get_module_or_404
from features.spaces.validators import get_space_or_404
from features.tasks.exceptions import TestIsNotPublic
from features.tasks.schemas import TestRead, TestUpdate, TestCreate
from features.tasks.validators import get_task_or_404, get_test_or_404


async def create_test(
    session: AsyncSession,
    user_id: int,
    test_in: TestCreate,
) -> TestRead:
    task = await get_task_or_404(session, test_in.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)
    check_user_is_admin_or_owner(account.role)

    test = await test_crud.create_test(session, test_in)
    return test.get_validation_schema()


async def update_test(
    session: AsyncSession,
    user_id: int,
    test_id: int,
    test_update: TestUpdate,
) -> TestRead:
    test = await get_test_or_404(session, test_id)
    task = await get_task_or_404(session, test.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)
    update_data = test_update.model_dump(exclude_unset=True)

    test = await test_crud.update_test(session, test, update_data)
    return test.get_validation_schema()


async def get_test_by_id(
    session: AsyncSession,
    user_id: int,
    test_id: int,
) -> TestRead:
    test = await get_test_or_404(session, test_id)
    task = await get_task_or_404(session, test.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    _ = await get_account_or_404(session, user_id, module.space_id)

    if not test.is_public:
        raise TestIsNotPublic()
    return test.get_validation_schema()


async def delete_test(
    session: AsyncSession,
    test_id: int,
    user_id: int,
) -> None:
    test = await get_test_or_404(session, test_id)
    task = await get_task_or_404(session, test.task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    account = await get_account_or_404(session, user_id, module.space_id)

    check_user_is_admin_or_owner(account.role)

    await test_crud.delete_test(session, test)


async def get_tests_in_task(
    session: AsyncSession,
    user_id: int,
    task_id: int,
) -> list[TestRead]:
    task = await get_task_or_404(session, task_id)
    module = await get_module_or_404(session, task.module_id)
    _ = await get_space_or_404(session, module.space_id)
    _ = await get_account_or_404(session, user_id, module.space_id)

    tests = await test_crud.get_tests_by_task_id(session, task_id)
    if not tests:
        return []
    tests = [test for test in tests if test.is_public]
    return mapper.build_test_read_list(tests)
