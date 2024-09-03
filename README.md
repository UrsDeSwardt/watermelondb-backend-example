# watermelondb-backend-example

## Setup

### Requirements

- docker

### Linux and macOS

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```shell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Dev

```shell
fastapi dev
```

### Migrations

```shell
alembic revision --autogenerate -m "comment"
```

```shell
alembic upgrade head
```


## Test

```shell
pytest
```

## Deploy

```shell
docker build -t watermelondb-backend-example .
```

```shell
docker run -p 8000:80 watermelondb-backend-example
```
