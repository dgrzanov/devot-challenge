# Devot challenge

## Setting up Python virtual environment

When initially starting the project create the virtual environment:

```bash
python3 -m venv .venv
```

Now activate the virtual environment from project root:

```bash
source .venv/bin/activate
```

Upgrade pip (to avoid potential problems later):

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Starting the DB server

The DB server is dockerized and can be easily started with:

```bash
docker compose up
```

If you are starting the database for the first time, migrate the tables from SQLModel models:

```bash
python src/migrate_tables.sql
```

This will create all the tables and fill the category table with initial data.

## Starting MW (DEV)

Start the FastAPI server:

```bash
fastapi dev src/main.py
```

## Swagger

Swagger can be accessed from http://localhost:8000/docs. Make sure you register the user you will be using on other endpoints.

After you've registered your user, log in by clicking the "Authorize" button in the top right corner.

After logging in successfully you can use the other endpoints.
