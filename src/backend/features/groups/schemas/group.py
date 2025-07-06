from features.accounts.schemas.account import AccountReadWithProfileData
from features.modules.schemas import ModuleReadWithPerformance
from features.spaces.schemas import (
    SpaceBase,
    SpaceCreate,
    SpaceRead,
    SpaceReadWithAccounts,
    SpaceReadWithModules,
    SpaceReadWithAccountsAndModules,
    SpaceUpdate,
)


class GroupBase(SpaceBase):
    pass


class GroupCreate(SpaceCreate):
    pass


class GroupRead(SpaceRead):
    def to_with_accounts(
        self,
        accounts: list[AccountReadWithProfileData],
    ) -> "GroupReadWithAccounts":
        return GroupReadWithAccounts(
            **self.model_dump(),
            accounts=accounts,
        )

    def to_with_modules(
        self,
        modules: list[ModuleReadWithPerformance],
    ) -> "GroupReadWithModules":
        return GroupReadWithModules(
            **self.model_dump(),
            modules=modules,
        )

    def to_with_accounts_and_modules(
        self,
        accounts: list[AccountReadWithProfileData],
        modules: list[ModuleReadWithPerformance],
    ) -> "GroupReadWithAccountsAndModules":
        return GroupReadWithAccountsAndModules(
            **self.model_dump(),
            accounts=accounts,
            modules=modules,
        )


class GroupReadWithAccounts(GroupRead, SpaceReadWithAccounts):
    pass


class GroupReadWithModules(GroupRead, SpaceReadWithModules):
    pass


class GroupReadWithAccountsAndModules(
    GroupReadWithAccounts, GroupReadWithModules, SpaceReadWithAccountsAndModules
):
    pass


class GroupUpdate(SpaceUpdate):
    pass
