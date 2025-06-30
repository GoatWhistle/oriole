import logging.config

try:
    from sentry_sdk.integrations.logging import EventHandler as SentryHandler

    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False


def setup_logging():
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": (
                    '{"time": "%(asctime)s", "level": "%(levelname)s", '
                    '"name": "%(name)s", "message": %(message)s}'
                )
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": "DEBUG",
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console"] + (["sentry"] if SENTRY_AVAILABLE else []),
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.error": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "": {
                "handlers": ["console"],
                "level": "WARNING",
            },
        },
    }

    if SENTRY_AVAILABLE:
        config["handlers"]["sentry"] = {
            "()": SentryHandler,
            "level": "ERROR",
        }

    logging.config.dictConfig(config)
