from main import app
from core.gunicorn_app import Application
from core.gunicorn_app import get_options
from core.config import settings


def main():
    gunicorn_app = Application(
        app=app,
        options=get_options(
            host=settings.run.host,
            port=settings.run.port,
            workers=settings.gunicorn_run.workers,
            timeout=settings.gunicorn_run.timeout,
        ),
    )
    gunicorn_app.run()


if __name__ == "__main__":
    main()
