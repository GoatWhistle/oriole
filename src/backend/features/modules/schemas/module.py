from datetime import datetime
from typing import Annotated, Optional, Sequence

from pydantic import BaseModel, Field, ConfigDict

from features.tasks.schemas import TaskReadPartial
from utils import get_number_one_bit_less as get_num_opt


class ModuleBase(BaseModel):
    title: Annotated[str, Field(max_length=get_num_opt(100))]
    description: Annotated[str, Field(max_length=get_num_opt(200))]

    is_contest: bool


class ModuleCreate(ModuleBase):
    group_id: int

    start_datetime: datetime
    end_datetime: datetime


class ModuleReadPartial(ModuleBase):
    id: int

    tasks_count: int
    user_completed_tasks_count: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class ModuleRead(ModuleReadPartial):
    group_id: int

    admin_id: int
    tasks: Sequence[TaskReadPartial]

    start_datetime: datetime
    end_datetime: datetime


class ModuleUpdate(ModuleBase):
    start_datetime: datetime
    end_datetime: datetime


class ModuleUpdatePartial(ModuleBase):
    title: Annotated[Optional[str], Field(max_length=get_num_opt(100))] = None
    description: Annotated[Optional[str], Field(max_length=get_num_opt(200))] = None

    is_contest: Optional[bool] = None

    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
