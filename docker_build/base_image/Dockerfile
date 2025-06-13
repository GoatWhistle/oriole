FROM python:3.13.0-bookworm AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /backend

RUN pip install --upgrade pip wheel "poetry==2.1.2"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev

COPY src/backend ./

FROM base AS migrations

RUN apt-get update && \
    apt-get install -y netcat-openbsd postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod +x pre_start.sh

CMD ["sh", "pre_start.sh"]

FROM base AS backend

RUN chmod +x gunicorn_run.py

CMD ["python", "./gunicorn_run.py"]

FROM base AS celery_worker
CMD ["celery", "-A", "core.celery.app", "worker", "--loglevel=info"]

FROM base AS celery_beat
CMD ["celery", "-A", "core.celery.app", "beat", "--loglevel=info"]
