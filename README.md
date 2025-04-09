# Devot challenge

## Starting the DB server

The DB server is dockerized and can be easily started with:

```bash
docker compose up
```

## Starting MW (DEV)

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

Start the FastAPI server:

```bash
fastapi dev src/main.py
```
