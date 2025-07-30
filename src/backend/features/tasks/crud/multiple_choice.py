from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import MultipleChoiceTask
from features.tasks.schemas import MultipleChoiceTaskCreate
from utils import get_current_utc


async def create_multiple_choice_task(
    session: AsyncSession,
    task_in: MultipleChoiceTaskCreate,
    account_id: int,
) -> MultipleChoiceTask:
    is_active = task_in.start_datetime <= get_current_utc() <= task_in.end_datetime
    task = MultipleChoiceTask(
        **task_in.model_dump(exclude={"is_active"}),
        is_active=is_active,
        creator_id=account_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
