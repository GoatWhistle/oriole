from pydantic import BaseModel, Field, ConfigDict

from features.groups.schemas import AccountRead
from features.modules.schemas import ModuleRead
from features.modules.schemas.module import (
    ModuleReadWithoutReplies,
    ModuleReadWithoutTasks,
)


class GroupBase(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int

    accounts: list[AccountRead]
    modules: list[ModuleRead | ModuleReadWithoutReplies | ModuleReadWithoutTasks]

    model_config = ConfigDict(from_attributes=True)


class GroupUpdate(GroupBase):
    pass


class GroupUpdatePartial(GroupUpdate):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=200)


class GroupReadWithoutModules(GroupBase):
    id: int
    accounts: list[AccountRead]
    model_config = ConfigDict(from_attributes=True)


class GroupReadWithoutAccounts(GroupBase):
    id: int
    modules: list[ModuleRead | ModuleReadWithoutReplies | ModuleReadWithoutTasks]
    model_config = ConfigDict(from_attributes=True)


class GroupReadWithoutModulesAndAccounts(GroupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
