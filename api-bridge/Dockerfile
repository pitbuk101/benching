FROM python:3.12-slim AS builder

RUN pip install poetry==2.0.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
FROM python:3.12-slim  AS runtime

RUN apt-get update && apt install -y netcat-traditional

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src src
COPY pyproject.toml pyproject.toml
ENTRYPOINT ["/app/.venv/bin/python", "-m", "uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "8088", "--loop", "uvloop", "--http", "httptools"]