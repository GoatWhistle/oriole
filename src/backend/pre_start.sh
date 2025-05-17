#!/bin/sh

DB_HOST=$(echo "$APP_CONFIG__DB__DB_URL" | sed -E 's|.+@([^:/]+):.*|\1|')
DB_PORT=$(echo "$APP_CONFIG__DB__DB_URL" | sed -E 's|.+:([0-9]+)/.*|\1|')

echo "Waiting connection to db ${DB_HOST}:${DB_PORT}..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "DB_URL: $APP_CONFIG__DB__DB_URL"
  echo "DB_HOST: $DB_HOST"
  echo "DB_PORT: $DB_PORT"
  echo "db not available..."
  sleep 1
done

echo "db available"
# сюды вставить создание миграции нужной
# alembic revision --autogenerate -m "твоё название"

alembic upgrade head

echo "Migrations completed"