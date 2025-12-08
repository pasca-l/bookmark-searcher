FROM python:3.14-slim AS builder

WORKDIR /app

# copy uv binaries from distroless image
# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.9.15 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

FROM ubuntu:latest AS migration

WORKDIR /app

RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y curl
# install Atlas CLI
RUN curl -sSf https://atlasgo.sh | sh

COPY atlas.hcl .
COPY app/db/schema/schema.sql ./app/db/schema/schema.sql

CMD ["sh", "-c", "atlas schema apply --env ${ATLAS_ENV:-local} --auto-approve"]

FROM python:3.14-slim AS server

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
