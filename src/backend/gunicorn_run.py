from core.config import settings
from core.gunicorn import Application, get_options
from main import app


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
