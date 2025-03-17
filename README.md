# severstal-test

## Assumptions:
1. I intentionally committed the `.env` file and `settings.toml` because the project is educational and needs to be quickly set up on the local machine of the reviewer. This solution is not for production purposes.

2. The task states: "Implement functionality to delete a coil with a specified ID. In case of success, return the deleted coil." I was confused. If this meant adding a new value to `deleted_at` field, I created the `update_coil` endpoint for better database management (e.g. someone used a piece of coil, so weight and length reduces). If, however, it meant "delete the record," then I created the `delete_coil` endpoint.

## How to run

1. Use Docker after `git clone ...`. It's hard to push to docker hub, because of assumption 1.

```shell
docker compose up -d
```
Web application is running on http://0.0.0.0:8081/docs / http://localhost:8081/docs

Adminer for easier database managment is running on http://localhost:8080/ (system = `PostgreSQL`, Server = `db`, username = `postgres`, password = `password`, database = `severstal_db`, but check the assumption 1 :) 

2. To run locally you need to set up database:
```shell
docker-compose -f docker-compose-dev.yml up -d
```

```shell
pip install poetry
poetry install
poetry run hypercorn main:app --reload
poetry alembic upgrade head
```
WARNING: Up venv python 3.11 and use first method to run :)

## Project Structure

```shell
severstal-test/
├── github/workflows
│   └── ci.yml
├── src/
│   ├── database
│   │   ├── alembic/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── middlware
│   │   └── log_middlware.py
│   ├── routes
│   │   ├── coils
│   │   │   ├── __init__.py
│   │   │   ├── abstract_data_storage.py
│   │   │   ├── dao.py
│   │   │   ├── database.py
│   │   │   ├── exceptions.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── healthchecks
│   │   │   ├── __init__.py
│   │   │   ├── schema.py
│   │   │   ├── spec.py
│   │   │   └── views.py
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── config_log.py
│   │   ├── settings.py
│   │   ├── utils.py
│   │   └── version.py
├── tests/                                  # Didn't have time to implement the tests
├── .dockerignore
├── .env                                    # Check assumption 1
├── .gitignore
├── alembic.ini
├── CHANGELOG.md
├── docker-compose-dev.yml                  # Configuration file for dev docker compose (no web) 
├── docker-compose.yml                      # Configuration file for "production" docker compose
├── Dockerfile
├── hypercorn.conf.py
├── main.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── settings.toml
```
