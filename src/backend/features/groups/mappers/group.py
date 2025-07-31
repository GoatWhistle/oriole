from features.accounts.mappers import build_account_read_with_profile_data_list
from features.accounts.models import Account
from features.groups.models import Group
from features.groups.schemas.group import (
    GroupRead,
    GroupReadWithAccounts,
    GroupReadWithAccountsAndModules,
    GroupReadWithModules,
)
from features.modules.mappers import build_module_read_with_progress_list
from features.modules.models import AccountModuleProgress, Module
from features.users.models import UserProfile


def build_group_read_with_accounts(
    group: Group,
    accounts: list[Account],
    user_profiles: list[UserProfile],
) -> GroupReadWithAccounts:
    accounts_schemas = build_account_read_with_profile_data_list(
        accounts, user_profiles
    )
    base_schema = group.get_validation_schema()

    return base_schema.to_with_accounts(accounts_schemas)


def build_group_read_with_modules(
    group: Group,
    modules: list[Module],
    account_module_progresses: list[AccountModuleProgress],
) -> GroupReadWithModules:
    base_schema = group.get_validation_schema()
    modules_schemas = build_module_read_with_progress_list(
        modules, account_module_progresses
    )

    return base_schema.to_with_modules(modules_schemas)


def build_group_read_with_accounts_and_modules(
    group: Group,
    accounts: list[Account],
    user_profiles: list[UserProfile],
    modules: list[Module],
    account_module_progresses: list[AccountModuleProgress],
) -> GroupReadWithAccountsAndModules:
    base_schema = group.get_validation_schema()
    accounts_schemas = build_account_read_with_profile_data_list(
        accounts, user_profiles
    )
    modules_schemas = build_module_read_with_progress_list(
        modules, account_module_progresses
    )

    return base_schema.to_with_accounts_and_modules(accounts_schemas, modules_schemas)


def build_group_read_list(groups: list[Group]) -> list[GroupRead]:
    return [group.get_validation_schema() for group in groups]
