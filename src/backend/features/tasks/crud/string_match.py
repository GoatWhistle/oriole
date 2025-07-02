from sqlalchemy.ext.asyncio import AsyncSession

from features.tasks.models import StringMatchTask
from features.tasks.schemas import StringMatchTaskCreate
from utils import get_current_utc


async def create_string_match_task(
    session: AsyncSession,
    task_data: StringMatchTaskCreate,
) -> StringMatchTask:
    is_active = task_data.start_datetime <= get_current_utc() <= task_data.end_datetime
    task = StringMatchTask(
        **task_data.model_dump(exclude={"is_active"}),
        is_active=is_active,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
