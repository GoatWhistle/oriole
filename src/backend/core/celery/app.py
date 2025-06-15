from celery import Celery


app = Celery(
    "core.celery.app",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
    broker_connection_retry_on_startup=True,
    include=["core.celery.tasks", "core.celery.email_tasks"],
)


app.conf.beat_schedule = {
    "check-deadlines-every-20-seconds": {
        "task": "core.celery.tasks.run_deadline_checks",
        "schedule": 20.0,
    }
}

app.autodiscover_tasks(["core.celery"])
