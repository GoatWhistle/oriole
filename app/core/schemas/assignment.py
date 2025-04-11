from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Sequence, Optional

from .group import GroupRead
from .user import UserRead
from .task import TaskRead


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    description: str
    is_contest: bool

    admin_id: int
    admin: UserRead

    group_id: int
    group: GroupRead

    tasks: Sequence[TaskRead]


class AssignmentRead(AssignmentBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(AssignmentCreate):
    pass


class AssignmentUpdatePartial(AssignmentCreate):
    title: Annotated[str, Field(max_length=100)] = None
    description: Optional[str] = None
    is_contest: bool = None

    admin_id: Optional[int] = None
    admin: Optional[UserRead] = None

    group_id: Optional[int] = None
    group: Optional[GroupRead] = None

    tasks: Sequence[TaskRead] = None
