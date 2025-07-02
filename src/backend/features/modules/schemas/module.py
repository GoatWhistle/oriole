from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ModuleBase(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)

    start_datetime: datetime
    end_datetime: datetime

    is_contest: bool


class ModuleCreate(ModuleBase):
    space_id: int


class ModuleRead(ModuleBase):
    id: int

    is_active: bool

    space_id: int
    creator_id: int

    tasks_count: int
    user_completed_tasks_count: int

    tasks: list

    model_config = ConfigDict(from_attributes=True)


class ModuleUpdate(ModuleBase):
    pass


class ModuleUpdatePartial(ModuleUpdate):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=200)

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None

    is_contest: bool | None = None


class ModuleReadWithoutReplies(ModuleBase):
    id: int

    is_active: bool

    space_id: int
    creator_id: int

    tasks_count: int
    user_completed_tasks_count: int

    tasks: list

    model_config = ConfigDict(from_attributes=True)


class ModuleReadWithoutTasks(ModuleBase):
    id: int

    is_active: bool

    space_id: int
    creator_id: int

    tasks_count: int

    model_config = ConfigDict(from_attributes=True)
