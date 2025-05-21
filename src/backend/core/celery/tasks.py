from core.models import db_helper
from crud.tasks import check_and_update_task_deadlines
from core.celery.celery_worker import celery_app
import asyncio


@celery_app.task
def check_task_deadlines():
    async def _check_deadlines():
        async with db_helper.get_async_session() as session:
            await check_and_update_task_deadlines(session=session)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_check_deadlines())
