from features.accounts.models import Account
from features.groups.mappers import build_account_read_list
from features.groups.models import Group
from features.groups.schemas import GroupRead
from features.groups.schemas.group import (
    GroupReadWithoutModules,
    GroupReadWithoutModulesAndAccounts,
    GroupReadWithoutAccounts,
)
from features.modules.mappers import build_module_read_list
from features.modules.models import Module
from features.solutions.models import BaseSolution
from features.tasks.models import StringMatchTask
from features.users.models import UserProfile


def build_group_read(
    group: Group,
    accounts: list[Account] | None = None,
    user_profiles: list[UserProfile] | None = None,
    modules: list[Module] | None = None,
    tasks: list[StringMatchTask] | None = None,
    user_replies: list[BaseSolution] | None = None,
) -> (
    GroupRead
    | GroupReadWithoutModules
    | GroupReadWithoutAccounts
    | GroupReadWithoutModulesAndAccounts
):
    account_reads = build_account_read_list(accounts or [], user_profiles or [])
    module_reads = build_module_read_list(
        modules or [], tasks or [], user_replies or []
    )
    base_data = {
        "id": group.id,
        "title": group.title,
        "description": group.description,
    }
    model_class: type[
        GroupRead
        | GroupReadWithoutModules
        | GroupReadWithoutAccounts
        | GroupReadWithoutModulesAndAccounts
    ]

    match (bool(accounts), bool(modules)):
        case (True, True):
            model_class = GroupRead
            extra_data = {"accounts": account_reads, "modules": module_reads}
        case (True, False):
            model_class = GroupReadWithoutModules
            extra_data = {"accounts": account_reads}
        case (False, True):
            model_class = GroupReadWithoutAccounts
            extra_data = {"modules": module_reads}
        case _:
            model_class = GroupReadWithoutModulesAndAccounts
            extra_data = {}

    return model_class(**base_data, **extra_data)


def build_group_read_list(
    groups: list[Group],
    accounts: list[Account] | None = None,
    user_profiles: list[UserProfile] | None = None,
    modules: list[Module] | None = None,
    tasks: list[StringMatchTask] | None = None,
    user_replies: list[BaseSolution] | None = None,
) -> list:
    accounts_by_group_id: dict[int, list[Account]] = {}
    modules = modules or []
    tasks = tasks or []
    user_replies = user_replies or []
    accounts = accounts or []
    user_profiles = user_profiles or []
    for account in accounts:
        accounts_by_group_id.setdefault(account.group_id, []).append(account)

    modules_by_group_id: dict[int, list[Module]] = {}
    for module in modules:
        modules_by_group_id.setdefault(module.group_id, []).append(module)

    tasks_by_module_id: dict[int, list[StringMatchTask]] = {}
    for task in tasks:
        tasks_by_module_id.setdefault(task.module_id, []).append(task)

    group_read_list: list = []

    for group in groups:
        group_accounts = accounts_by_group_id.get(group.id, [])
        group_modules = modules_by_group_id.get(group.id, [])

        group_module_ids = {module.id for module in group_modules}
        group_tasks = [task for task in tasks if task.module_id in group_module_ids]
        group_read_list.append(
            build_group_read(
                group,
                group_accounts,
                user_profiles,
                group_modules,
                group_tasks,
                user_replies,
            )
        )

    return group_read_list
