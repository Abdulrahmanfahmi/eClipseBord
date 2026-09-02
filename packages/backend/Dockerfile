FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages/backend/pyproject.toml packages/backend/pyproject.toml
COPY packages/frontend/pyproject.toml packages/frontend/pyproject.toml

RUN uv sync --frozen --no-dev --package backend

COPY packages/backend packages/backend
COPY data data

EXPOSE 8000

CMD ["uv", "run", "--package", "backend", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]