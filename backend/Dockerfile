FROM python:3.14-slim 

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set UV_LINK_MODE to avoid filesystem warnings
ENV UV_LINK_MODE=copy

RUN mkdir -p /app/logs && chmod 0777 /app/logs

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload"]