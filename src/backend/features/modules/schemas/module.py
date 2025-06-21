from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from features.tasks.schemas import TaskRead
from utils import get_number_one_bit_less as get_num_opt


class ModuleBase(BaseModel):
    title: str = Field(max_length=get_num_opt(100))
    description: str = Field(max_length=get_num_opt(200))

    start_datetime: datetime
    end_datetime: datetime

    is_contest: bool


class ModuleCreate(ModuleBase):
    group_id: int


class ModuleRead(ModuleBase):
    id: int

    is_active: bool

    group_id: int
    admin_id: int

    tasks_count: int
    user_completed_tasks_count: int

    tasks: list[TaskRead]

    model_config = ConfigDict(
        from_attributes=True,
    )


class ModuleUpdate(ModuleBase):
    pass


class ModuleUpdatePartial(ModuleUpdate):
    title: str | None = Field(default=None, max_length=get_num_opt(100))
    description: str | None = Field(default=None, max_length=get_num_opt(200))

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None

    is_contest: bool | None = None
