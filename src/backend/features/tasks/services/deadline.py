from sqlalchemy import select

from core.config import settings
from database import DbHelper
from features.tasks.models import Task
from utils.time_manager import get_current_utc


async def check_tasks_deadlines():
    local_db_helper = DbHelper(
        db_url=str(settings.db.db_url),
    )

    async with local_db_helper.session_factory() as session:
        current_time = get_current_utc()
        result = await session.execute(
            select(Task).where(
                (Task.start_datetime <= current_time)
                | (Task.end_datetime <= current_time)
            )
        )
        tasks = result.scalars().all()

        updated_count = 0
        for task in tasks:
            new_status = task.start_datetime <= current_time <= task.end_datetime
            if task.is_active != new_status:
                task.is_active = new_status
                updated_count += 1

        if updated_count > 0:
            await session.commit()

        await local_db_helper.dispose()

        return updated_count
