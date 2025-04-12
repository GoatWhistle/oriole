from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, Sequence


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=64)]
    description: Annotated[str, Field(max_length=200)]

    accounts: Sequence[int]
    assignments: Sequence[int]


class GroupRead(GroupBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupCreate):
    pass


class GroupUpdatePartial(GroupCreate):
    title: Annotated[Optional[str], Field(max_length=64)] = None
    description: Annotated[Optional[str], Field(max_length=200)] = None

    accounts: Sequence[int] = None
    assignments: Sequence[int] = None
