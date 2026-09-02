FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages/backend/pyproject.toml packages/backend/pyproject.toml
COPY packages/frontend/pyproject.toml packages/frontend/pyproject.toml

RUN uv sync --frozen --no-dev --package frontend

COPY packages/frontend packages/frontend

EXPOSE 8501

CMD ["uv", "run", "--package", "frontend", "streamlit", "run", "packages/frontend/src/frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501"]