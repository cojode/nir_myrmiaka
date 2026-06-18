FROM python:bookworm as prod

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

RUN pip install uv

ENV UV_NO_VENV=1
ENV UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/tmp/uv_cache \
    uv sync --no-dev --no-install-project --no-editable

COPY . .

RUN uv sync --no-dev --no-editable

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "-m", "nir_myrmiaka"]

FROM prod as dev

RUN --mount=type=cache,target=/tmp/uv_cache \
    uv sync --no-install-project --no-editable