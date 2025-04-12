from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Sequence, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .group import GroupRead
    from .user import UserRead
    from .task import TaskRead


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    description: str
    is_contest: bool

    admin_id: int

    group_id: int

    tasks: Sequence[int]


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

    group_id: Optional[int] = None

    tasks: Sequence[int] = None
