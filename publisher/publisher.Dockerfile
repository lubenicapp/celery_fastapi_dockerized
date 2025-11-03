FROM python:3.14-slim
ENTRYPOINT ["uv", "run", "uvicorn", "publisher.app:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy pyproject.toml and install dependencies with uv
COPY pyproject.toml ./
COPY uv.lock* ./
RUN uv sync --locked

COPY .  ./publisher
