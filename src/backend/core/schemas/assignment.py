from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional, Sequence

from core.schemas.task import TaskReadPartial
from utils.number_optimizer import get_number_one_bit_less as num_opt


class AssignmentBase(BaseModel):
    title: Annotated[str, Field(max_length=num_opt(100))]
    description: Annotated[str, Field(max_length=num_opt(200))]

    is_contest: bool

class AssignmentReadPartial(AssignmentBase):
    id: int

    tasks_count: int
    user_completed_tasks_count: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

class AssignmentRead(AssignmentReadPartial):
    group_id: int

    admin_id: int
    tasks: Sequence[TaskReadPartial]

    start_datetime: datetime
    end_datetime: datetime


class AssignmentCreate(AssignmentBase):
    group_id: int

    start_datetime: datetime
    end_datetime: datetime


class AssignmentUpdate(AssignmentBase):
    start_datetime: datetime
    end_datetime: datetime


class AssignmentUpdatePartial(AssignmentBase):
    title: Annotated[Optional[str], Field(max_length=num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=num_opt(200))] = None

    is_contest: Optional[bool] = None

    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

