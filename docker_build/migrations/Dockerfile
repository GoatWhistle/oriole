FROM python:3.13.0-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y netcat-openbsd postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip wheel "poetry==2.1.1"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY src/backend ./

RUN chmod +x pre_start.sh

CMD ["sh", "pre_start.sh"]