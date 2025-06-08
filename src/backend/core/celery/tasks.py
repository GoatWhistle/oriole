import asyncio

from celery import shared_task

from modules.services.deadline import check_modules_deadlines
from tasks.services.deadline import check_tasks_deadlines


@shared_task
def run_deadline_checks():
    asyncio.run(_run_all_deadline_checks())


async def _run_all_deadline_checks():
    await check_tasks_deadlines()
    await check_modules_deadlines()
