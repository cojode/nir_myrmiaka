FROM python:3.11.4-slim-bullseye as prod

# Install system dependencies
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.2

# Configure Poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Set working directory and copy files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install main dependencies (including your package in editable mode)
RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set PYTHONPATH to ensure package discovery
ENV PYTHONPATH=/app

# Entrypoint and command (run through Poetry)
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["poetry", "run", "python", "-m", "nir_myrmiaka"]

FROM prod as dev
# Install dev dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --no-interaction --no-ansi