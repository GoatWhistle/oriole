from pydantic import Field

from features.solutions.schemas import (
    BaseSolutionModel,
    BaseSolutionCreate,
    BaseSolutionRead,
)


class StringMatchSolutionBase(BaseSolutionModel):
    pass


class StringMatchSolutionCreate(StringMatchSolutionBase, BaseSolutionCreate):
    user_answer: str = Field(max_length=300)


class StringMatchSolutionRead(StringMatchSolutionBase, BaseSolutionRead):
    pass
