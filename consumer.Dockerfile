FROM python:3.14-slim
ENTRYPOINT ["uv", "run", "celery", "-A", "consumer.event_investigation", "worker"]
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy pyproject.toml and install dependencies with uv
COPY pyproject.toml ./
COPY uv.lock* ./

RUN uv sync --locked

COPY ./consumer ./consumer
