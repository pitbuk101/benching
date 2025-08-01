# reference: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.12-slim AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --without dev,eval,demo,test --no-root && rm -rf ${POETRY_CACHE_DIR}
FROM python:3.12-slim AS runtime

RUN apt-get update && apt install -y netcat-traditional

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src src
# COPY source_ai.xlsx source_ai.xlsx
COPY entrypoint.sh /app/entrypoint.sh
COPY ./config.yaml /app/data/config.yaml
COPY pyproject.toml pyproject.toml
RUN chmod +x /app/entrypoint.sh
ENV EXAMPLES="src/source_ai"
ENTRYPOINT [ "/app/entrypoint.sh" ]