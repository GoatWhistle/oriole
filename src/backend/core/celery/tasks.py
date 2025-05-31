from celery import shared_task
from crud.tasks import check_task_deadlines
from crud.assignments import check_assignment_deadlines
import asyncio


@shared_task
def run_deadline_checks():
    asyncio.run(_run_all_deadline_checks())


async def _run_all_deadline_checks():
    await check_task_deadlines()
    await check_assignment_deadlines()
