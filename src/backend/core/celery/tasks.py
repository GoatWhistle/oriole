import asyncio

from celery import shared_task

from features.modules.crud.module import update_modules_activity
from features.tasks.crud.base import update_tasks_activity


@shared_task
def run_deadline_checks():
    asyncio.run(_run_all_deadline_checks())


async def _run_all_deadline_checks():
    await update_tasks_activity()
    await update_modules_activity()
