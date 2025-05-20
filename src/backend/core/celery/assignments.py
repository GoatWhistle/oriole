from core.models import db_helper
from crud.assignments import check_and_update_assignment_deadlines
from core.celery.celery_worker import celery_app


@celery_app.task
async def check_deadlines():
    async with db_helper.get_async_session() as session:
        await check_and_update_assignment_deadlines(session)
