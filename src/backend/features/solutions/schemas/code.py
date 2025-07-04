from features.solutions.schemas import BaseSolutionModel
from features.solutions.schemas.base import BaseSolutionCreate, BaseSolutionRead


class CodeSolutionBase(BaseSolutionModel):
    code: str


class CodeSolutionCreate(CodeSolutionBase, BaseSolutionCreate):
    pass


class CodeSolutionRead(CodeSolutionBase, BaseSolutionRead):
    pass
