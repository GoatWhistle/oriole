from features.tasks.schemas import (
    BaseTaskModel,
    BaseTaskRead,
    BaseTaskCreate,
    BaseTaskUpdate,
)


class CodeTaskBase(BaseTaskModel):
    time_limit: int
    memory_limit: int


class CodeTaskCreate(CodeTaskBase, BaseTaskCreate):
    pass


class CodeTaskRead(CodeTaskBase, BaseTaskRead):
    tests: list


class CodeTaskUpdate(CodeTaskBase):
    pass


class CodeTaskUpdatePartial(CodeTaskUpdate, BaseTaskUpdate):
    time_limit: int | None = None
    memory_limit: int | None = None
