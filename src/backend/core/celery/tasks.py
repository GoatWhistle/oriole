import asyncio

from celery import shared_task

from features.groups.crud.group_invite import update_group_invites_activity
from features.modules.crud.module import update_modules_activity
from features.tasks.crud.base import update_tasks_activity


@shared_task
def run_activity_checks():
    asyncio.run(_run_all_activity_checks())


async def _run_all_activity_checks():
    await update_tasks_activity()
    await update_modules_activity()
    await update_group_invites_activity()
