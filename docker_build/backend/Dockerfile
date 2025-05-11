FROM python:3.13.0-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /backend

RUN pip install --upgrade pip wheel "poetry==2.1.1"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY src/backend ./

RUN chmod +x pre_start.sh
RUN chmod +x gunicorn_run.py

ENTRYPOINT ["./pre_start.sh"]
CMD ["python", "./gunicorn_run.py"]
