from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(
        self,
        app: FastAPI,
        options: dict,
    ):
        self.app = app
        self.options = options
        super().__init__()

    @property
    def config_options(self) -> dict:
        return {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }

    def load_config(self):
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.app


def get_options(
    host: str,
    port: int,
    workers: int,
    timeout: int,
) -> dict:
    return {
        "bind": f"{host}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
        "timeout": timeout,
    }
