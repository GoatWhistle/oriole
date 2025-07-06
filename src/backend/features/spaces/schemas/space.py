from pydantic import BaseModel, Field, ConfigDict

from features.accounts.schemas import AccountReadWithProfileData
from features.modules.schemas import ModuleReadWithPerformance


class SpaceBase(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)


class SpaceCreate(SpaceBase):
    pass


class SpaceRead(SpaceBase):
    id: int

    creator_id: int

    model_config = ConfigDict(from_attributes=True)

    def to_with_accounts(
        self,
        accounts: list[AccountReadWithProfileData],
    ) -> "SpaceReadWithAccounts":
        return SpaceReadWithAccounts(
            **self.model_dump(),
            accounts=accounts,
        )

    def to_with_modules(
        self,
        modules: list[ModuleReadWithPerformance],
    ) -> "SpaceReadWithModules":
        return SpaceReadWithModules(
            **self.model_dump(),
            modules=modules,
        )

    def to_with_accounts_and_modules(
        self,
        accounts: list[AccountReadWithProfileData],
        modules: list[ModuleReadWithPerformance],
    ) -> "SpaceReadWithAccountsAndModules":
        return SpaceReadWithAccountsAndModules(
            **self.model_dump(),
            accounts=accounts,
            modules=modules,
        )


class SpaceReadWithAccounts(SpaceRead):
    accounts: list[AccountReadWithProfileData]


class SpaceReadWithModules(SpaceRead):
    modules: list[ModuleReadWithPerformance]


class SpaceReadWithAccountsAndModules(SpaceReadWithAccounts, SpaceReadWithModules):
    pass


class SpaceUpdate(SpaceBase):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=200)
