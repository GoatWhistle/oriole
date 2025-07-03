from pydantic import BaseModel, ConfigDict


class TestBase(BaseModel):
    correct_output: str
    is_public: bool
    input_data: str | None = None


class TestCreate(TestBase):
    task_id: int


class TestRead(TestBase):
    id: int
    task_id: int
    module_id: int
    space_id: int

    model_config = ConfigDict(from_attributes=True)


class TestUpdate(TestBase):
    pass


class TestUpdatePartial(TestUpdate):
    correct_output: str | None = None
    if_public: str | None = None
    input_data: str | None = None
