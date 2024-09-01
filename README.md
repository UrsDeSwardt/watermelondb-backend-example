# watermelondb-backend-example

## Setup


### Linux and macOS

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```


## Run

```shell
docker build -t watermelondb-backend-example .
```

```shell
docker run -p 8000:80 watermelondb-backend-example
```