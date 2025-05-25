import asyncio
import asyncpg
from apscheduler.schedulers.background import BackgroundScheduler
from core.models.db_helper import db_helper

from crud.assignments import check_assignment_deadlines
from crud.tasks import check_task_deadlines


class TaskRunner:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def _execute_with_retry(self, task_func, max_retries=3):
        for attempt in range(max_retries):
            try:
                async with db_helper.session_factory() as session:
                    result = await task_func(session)
                    await session.commit()
                    return result
            except (RuntimeError, asyncpg.exceptions.PostgresError) as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
                continue

    def run_task(self, task_func):
        try:
            return self.loop.run_until_complete(self._execute_with_retry(task_func))
        finally:
            # Очистка pending tasks
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
            self.loop.close()

task_runner = TaskRunner()

scheduler = BackgroundScheduler(
    job_defaults={
        "max_instances": 1,
        "misfire_grace_time": 300
    },
    timezone="UTC"
)

def setup_scheduler():
    scheduler.add_job(
        lambda: task_runner.run_task(check_task_deadlines),
        "interval",
        minutes=3,
        id="task_deadlines"
    )

    scheduler.add_job(
        lambda: task_runner.run_task(check_assignment_deadlines),
        "interval",
        minutes=3,
        id="assignment_deadlines"
    )