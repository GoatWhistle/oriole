from typing import Annotated, Optional, Sequence

from pydantic import BaseModel, Field, ConfigDict

from groups.schemas import AccountReadPartial
from modules.schemas import ModuleReadPartial
from utils import get_number_one_bit_less as num_opt


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]


class GroupCreate(GroupBase):
    pass


class GroupReadPartial(GroupBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class GroupRead(GroupReadPartial):
    accounts: Sequence[AccountReadPartial]
    modules: Sequence[ModuleReadPartial]


class GroupUpdate(GroupCreate):
    pass


class GroupUpdatePartial(GroupCreate):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None
