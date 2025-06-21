from features.groups.mappers import build_account_read_list
from features.groups.models import Group, Account
from features.groups.schemas import GroupRead, AccountRead
from features.modules.mappers import build_module_read_list
from features.modules.models import Module
from features.modules.schemas import ModuleRead
from features.tasks.models import Task, UserReply
from features.users.models import UserProfile


def build_group_read(
    group: Group,
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module] | None = None,
    tasks: list[Task] | None = None,
    user_replies: list[UserReply] | None = None,
) -> GroupRead:
    modules = modules or []
    tasks = tasks or []
    user_replies = user_replies or []

    account_reads: list[AccountRead] = build_account_read_list(accounts, user_profiles)

    module_reads: list[ModuleRead] = build_module_read_list(
        modules=modules,
        tasks=tasks,
        user_replies=user_replies,
    )

    return GroupRead(
        id=group.id,
        title=group.title,
        description=group.description,
        accounts=account_reads,
        modules=module_reads,
    )


def build_group_read_list(
    groups: list[Group],
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module],
    tasks: list[Task],
    user_replies: list[UserReply],
) -> list[GroupRead]:
    accounts_by_group_id: dict[int, list[Account]] = {}
    for account in accounts:
        accounts_by_group_id.setdefault(account.group_id, []).append(account)

    modules_by_group_id: dict[int, list[Module]] = {}
    for module in modules:
        modules_by_group_id.setdefault(module.group_id, []).append(module)

    tasks_by_module_id: dict[int, list[Task]] = {}
    for task in tasks:
        tasks_by_module_id.setdefault(task.module_id, []).append(task)

    group_read_list: list[GroupRead] = []

    for group in groups:
        group_accounts = accounts_by_group_id.get(group.id, [])
        group_modules = modules_by_group_id.get(group.id, [])

        account_reads: list[AccountRead] = build_account_read_list(
            group_accounts, user_profiles
        )

        group_module_ids = {module.id for module in group_modules}
        group_tasks = [task for task in tasks if task.module_id in group_module_ids]

        module_reads = build_module_read_list(group_modules, group_tasks, user_replies)

        group_read_list.append(
            GroupRead(
                title=group.title,
                description=group.description,
                id=group.id,
                accounts=account_reads,
                modules=module_reads,
            )
        )

    return group_read_list
