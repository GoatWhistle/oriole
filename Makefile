.RECIPEPREFIX = >  # Теперь команды начинаются с '>'
.PHONY: up down re test

up:
> docker compose --env-file src/backend/.env build
> docker compose --env-file src/backend/.env up -d

down:
> docker compose down

re:
> docker compose down
> docker compose --env-file src/backend/.env build
> docker compose --env-file src/backend/.env up -d

test:
> PYTHONPATH=src/backend pytest src/tests/
