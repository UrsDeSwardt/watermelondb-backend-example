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
