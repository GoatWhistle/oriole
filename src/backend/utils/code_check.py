import os

from core.config import BASE_DIR
from shared.exceptions.existence import LanguageNotFountException


def get_runtime_or_404(language: str):
    runtimes = {
        "Python": {
            "image": "runner-python:3.9",
            "build_path": os.path.join(BASE_DIR, "core/celery/runtimes/python"),
            "command": lambda code: ["python", "-c", code],
        },
        "JavaScript": {
            "image": "runner-js:20",
            "build_path": os.path.join(BASE_DIR, "core/celery/runtimes/javascript"),
            "command": lambda code: ["node", "-e", code],
        },
    }
    if language not in runtimes:
        raise LanguageNotFountException()
    return runtimes[language]
