from core.models import db_helper
from crud.tasks import check_and_update_task_deadlines
from core.celery.celery_worker import celery_app


@celery_app.task
async def check_deadlines():
    async with db_helper.get_async_session() as session:
        await check_and_update_task_deadlines(session)
