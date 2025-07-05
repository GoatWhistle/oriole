from features.solutions.schemas import BaseSolutionModel
from features.solutions.schemas.base import BaseSolutionCreate, BaseSolutionRead


class CodeSolutionBase(BaseSolutionModel):
    code: str
    task_id: int


class CodeSolutionCreate(CodeSolutionBase, BaseSolutionCreate):
    pass


class CodeSolutionRead(CodeSolutionBase, BaseSolutionRead):
    pass
