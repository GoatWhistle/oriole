from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional, Sequence

from .assignment import AssignmentRead
from .user import UserRead


class GroupBase(BaseModel):
    title: Annotated[str, Field(max_length=64)]
    description: Annotated[str, Field(max_length=200)]

    admin_id: int
    admin: UserRead

    users: Sequence[UserRead]
    assignments: Sequence[AssignmentRead]


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

    admin_id: Optional[int] = None
    admin: Optional[UserRead] = None

    users: Sequence[UserRead] = None
    assignments: Sequence[AssignmentRead] = None
