from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional, Sequence

from core.schemas.account import AccountRead
from core.schemas.assignment import AssignmentRead

from utils.number_optimizer import get_number_one_bit_less as num_opt


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]


class GroupRead(GroupBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

class GroupDataRead(GroupRead):
    accounts: Sequence[AccountRead]
    assignments: Sequence[AssignmentRead]


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupCreate):
    pass


class GroupUpdatePartial(GroupCreate):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None
