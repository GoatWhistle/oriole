from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional, Sequence

from core.schemas.task import TaskRead
from utils.number_optimizer import get_number_one_bit_less as num_opt


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]

    is_contest: bool


class AssignmentRead(AssignmentBase):
    id: int
    admin_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class AssignmentDataRead(AssignmentRead):
    tasks: Sequence[TaskRead]


class AssignmentCreate(AssignmentBase):
    group_id: int


class AssignmentUpdate(AssignmentBase):
    pass


class AssignmentUpdatePartial(AssignmentBase):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None

    is_contest: Optional[bool] = None

