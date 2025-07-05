from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from features.tasks.schemas import BaseTaskReadWithCorrectness


class ModuleBase(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)

    start_datetime: datetime
    end_datetime: datetime


class ModuleCreate(ModuleBase):
    space_id: int


class ModuleRead(ModuleBase):
    id: int

    space_id: int
    creator_id: int

    tasks_count: int

    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    def to_with_performance(
        self, user_completed_tasks_count: int
    ) -> "ModuleReadWithPerformance":
        return ModuleReadWithPerformance(
            **self.model_dump(), user_completed_tasks_count=user_completed_tasks_count
        )

    def to_with_tasks(
        self,
        user_completed_tasks_count: int,
        tasks: list[BaseTaskReadWithCorrectness],
    ) -> "ModuleReadWithTasks":
        return ModuleReadWithTasks(
            **self.model_dump(),
            user_completed_tasks_count=user_completed_tasks_count,
            tasks=tasks,
        )


class ModuleReadWithPerformance(ModuleRead):
    user_completed_tasks_count: int


class ModuleReadWithTasks(ModuleReadWithPerformance):
    tasks: list[BaseTaskReadWithCorrectness]


class ModuleUpdate(ModuleBase):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=200)

    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
