import os

import uvicorn

from core.config import settings
from core.gunicorn import Application, get_options
from main import app


def main():
    is_dev = os.getenv("IS_DEV", "false").lower() == "true"
    if not (is_dev):
        gunicorn_app = Application(
            app=app,
            options=get_options(
                host=settings.run.host,
                port=settings.run.port,
                workers=settings.gunicorn_run.workers,
                timeout=settings.gunicorn_run.timeout,
                worker_class=settings.gunicorn_run.worker_class,
                reload=is_dev,
            ),
        )
        gunicorn_app.run()
    else:
        uvicorn.run(
            "main:app",
            host=settings.run.host,
            port=settings.run.port,
            reload=True,
        )


if __name__ == "__main__":
    main()
