FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system --no-cache -r <(uv pip compile pyproject.toml 2>/dev/null || echo "fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings httpx python-multipart") || pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings httpx python-multipart

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
