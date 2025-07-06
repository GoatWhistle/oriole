from features.accounts.mappers import build_account_read_with_profile_data_list
from features.accounts.models import Account
from features.groups.models import Group
from features.groups.schemas.group import (
    GroupReadWithModules,
    GroupReadWithAccounts,
    GroupReadWithAccountsAndModules,
    GroupRead,
)
from features.modules.mappers import build_module_read_with_performance_list
from features.modules.models import Module
from features.solutions.models import BaseSolution
from features.tasks.models import BaseTask
from features.users.models import UserProfile


def build_group_read_with_accounts(
    group: Group, accounts: list[Account], user_profiles: list[UserProfile]
) -> GroupReadWithAccounts:
    accounts_schemas = build_account_read_with_profile_data_list(
        accounts, user_profiles
    )
    base_schema = group.get_validation_schema()

    return base_schema.to_with_accounts(accounts_schemas)


def build_group_read_with_modules(
    group: Group,
    modules: list[Module],
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> GroupReadWithModules:
    modules_schemas = build_module_read_with_performance_list(modules, tasks, solutions)
    base_schema = group.get_validation_schema()

    return base_schema.to_with_modules(modules_schemas)


def build_group_read_with_accounts_and_modules(
    group: Group,
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module],
    tasks: list[BaseTask],
    solutions: list[BaseSolution],
) -> GroupReadWithAccountsAndModules:
    accounts_schemas = build_account_read_with_profile_data_list(
        accounts, user_profiles
    )
    modules_schemas = build_module_read_with_performance_list(modules, tasks, solutions)
    base_schema = group.get_validation_schema()

    return base_schema.to_with_accounts_and_modules(accounts_schemas, modules_schemas)


def build_group_read_list(groups: list[Group]) -> list[GroupRead]:
    return [group.get_validation_schema() for group in groups]
