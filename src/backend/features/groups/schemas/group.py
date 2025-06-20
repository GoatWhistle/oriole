from pydantic import BaseModel, Field, ConfigDict

from features.groups.schemas import AccountRead
from features.modules.schemas import ModuleRead
from utils import get_number_one_bit_less as get_num_opt


class GroupBase(BaseModel):
    title: str = Field(max_length=get_num_opt(100))
    description: str = Field(max_length=get_num_opt(200))


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: int

    accounts: list[AccountRead]
    modules: list[ModuleRead]

    model_config = ConfigDict(
        from_attributes=True,
    )


class GroupUpdate(GroupBase):
    pass


class GroupUpdatePartial(GroupUpdate):
    title: str | None = Field(default=None, max_length=get_num_opt(100))
    description: str | None = Field(default=None, max_length=get_num_opt(200))
