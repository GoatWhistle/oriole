from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import StringMatchSolution
from features.tasks.models import StringMatchTask
from shared.enums import TaskTypeEnum


async def create_string_match_solution(
    session: AsyncSession,
    account_id: int,
    task: StringMatchTask,
    user_answer: str,
) -> StringMatchSolution:
    solution = StringMatchSolution(
        account_id=account_id,
        task_id=task.id,
        answer={"user_answer": user_answer},
        is_correct=(user_answer == task.correct_answer),
        attempts=1,
        task_type=TaskTypeEnum.STRING_MATCH.value,
    )
    session.add(solution)
    await session.commit()
    await session.refresh(solution)
    return solution


async def update_string_match_solution(
    session: AsyncSession,
    solution: StringMatchSolution,
    user_answer: str,
) -> StringMatchSolution:
    solution.answer = {"user_answer": user_answer}
    solution.is_correct = user_answer == solution.task.correct_answer
    solution.user_attempts += 1

    await session.commit()
    await session.refresh(solution)
    return solution


async def delete_string_match_solution(
    session: AsyncSession,
    string_match_solution: StringMatchSolution,
) -> None:
    await session.delete(string_match_solution)
    await session.commit()
