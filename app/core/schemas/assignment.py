from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Sequence, Optional

from datetime import datetime

from .group import GroupRead
from .user import UserRead
from .task import TaskRead


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    description: str

    tasks: Sequence[TaskRead]
    progress: Sequence[UserRead]
    deadline: datetime

    group: GroupRead
    group_id: int

    admin: UserRead
    admin_id: int


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentRead(AssignmentCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class AssignmentUpdate(AssignmentCreate):
    pass


class AssignmentUpdatePartial(AssignmentCreate):
    title: Annotated[Optional[str], Field(max_length=100)]
    description: Optional[str]

    tasks: Sequence[Optional[TaskRead]]
    progress: Sequence[Optional[UserRead]]
    deadline: Optional[datetime]

    group: Optional[GroupRead]
    group_id: Optional[int]

    admin: Optional[UserRead]
    admin_id: Optional[int]
