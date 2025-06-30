#!/bin/sh

DB_HOST=$(echo "$DB_URL" | sed -E 's|.+@([^:/]+):.*|\1|')
DB_PORT=$(echo "$DB_URL" | sed -E 's|.+:([0-9]+)/.*|\1|')

echo "Waiting connection to db ${DB_HOST}:${DB_PORT}..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "DB_URL: $DB_URL"
  echo "DB_HOST: $DB_HOST"
  echo "DB_PORT: $DB_PORT"
  echo "db not available..."
  sleep 1
done

echo "db available"

alembic upgrade head
alembic current

echo "Migrations completed"
