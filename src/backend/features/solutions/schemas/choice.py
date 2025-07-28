from features.solutions.schemas import (
    BaseSolutionModel,
    BaseSolutionCreate,
    BaseSolutionRead,
)


class MultipleChoiceSolutionBase(BaseSolutionModel):
    pass


class MultipleChoiceSolutionCreate(MultipleChoiceSolutionBase, BaseSolutionCreate):
    user_answer: list


class MultipleChoiceSolutionRead(MultipleChoiceSolutionBase, BaseSolutionRead):
    pass

