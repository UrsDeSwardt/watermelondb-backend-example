# Watermelondb Backend Example

This is an example of a backend for [WatermelonDB](https://watermelondb.dev/docs) using [FastAPI](https://fastapi.tiangolo.com/).
The frontend of this example can be found [here](https://github.com/UrsDeSwardt/watermelondb-nextjs-example).

## Requirements

- [docker](https://www.docker.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation)

## Running the example

Ensure the database is running:

```shell
docker compose up db
```

Run the dev server:

```shell
fastapi dev
```

## Testing

```shell
pytest
```

### Migrations

```shell
alembic revision --autogenerate -m "comment"
```

```shell
alembic upgrade head
```
