FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ARG APP_PORT=8080
ARG APP_HOST=0.0.0.0

ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

EXPOSE ${APP_PORT}

CMD ["sh", "-c", "uv run fastapi run main.py --host $APP_HOST --port $APP_PORT"]