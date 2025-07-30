from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.solutions.models import SolutionFeedback
from features.solutions.schemas import SolutionFeedbackCreate
from utils import get_current_utc


async def create_solution_feedback(
    session: AsyncSession,
    solution_feedback_create: SolutionFeedbackCreate,
    solution_id: int,
    account_id: int,
) -> SolutionFeedback:
    solution_feedback = SolutionFeedback(
        **solution_feedback_create.model_dump(),
        solution_id=solution_id,
        creator_id=account_id,
        updated_at=get_current_utc(),
        is_updated=False,
    )
    session.add(solution_feedback)
    await session.commit()
    await session.refresh(solution_feedback)
    return solution_feedback


async def get_solution_feedback(
    session: AsyncSession,
    solution_feedback_id: int,
) -> SolutionFeedback | None:
    return await session.get(SolutionFeedback, solution_feedback_id)


async def get_feedbacks_by_solution_id(
    session: AsyncSession,
    solution_id: int,
) -> list[SolutionFeedback]:
    result = await session.execute(
        select(SolutionFeedback).where(SolutionFeedback.solution_id == solution_id)
    )
    return list(result.scalars().all())


async def update_solution_feedback(
    session: AsyncSession,
    solution_feedback: SolutionFeedback,
    solution_feedback_update: dict[str, Any],
) -> SolutionFeedback:
    if solution_feedback_update:
        for key, value in solution_feedback_update.items():
            setattr(solution_feedback, key, value)
        setattr(solution_feedback, "updated_at", get_current_utc())
        setattr(solution_feedback, "is_updated", True)
    await session.commit()
    await session.refresh(solution_feedback)
    return solution_feedback


async def delete_solution_feedback(
    session: AsyncSession,
    solution_feedback: SolutionFeedback,
) -> None:
    await session.delete(solution_feedback)
    await session.commit()
