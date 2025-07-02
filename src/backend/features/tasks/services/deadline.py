import features.tasks.crud.base as task_crud
from core.config import settings
from database import DbHelper
from utils import get_current_utc


async def check_tasks_deadlines():
    local_db_helper = DbHelper(url=str(settings.db.url))

    async with local_db_helper.session_factory() as session:
        tasks = await task_crud.get_tasks(session)

        updated = False
        for task in tasks:
            new_status = task.start_datetime <= get_current_utc() <= task.end_datetime
            if task.is_active != new_status:
                task.is_active = new_status
                updated = True

        if updated:
            await session.commit()

        await local_db_helper.dispose()
