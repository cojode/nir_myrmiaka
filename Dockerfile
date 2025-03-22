FROM python:3.11.4-slim-bullseye as prod

# Install SQLite3 (required for running sqlite3 commands)
RUN apt-get update && apt-get install -y sqlite3

# Install Poetry
RUN pip install poetry==1.8.2

# Configure Poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements (including Alembic)
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Copying the actual application and Alembic configuration
COPY . /app/src/

# Make the entrypoint script executable
RUN chmod +x /app/src/entrypoint.sh

# Install application dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Set the entrypoint script
ENTRYPOINT ["sh", "/app/src/entrypoint.sh"]

# Default command to run the application
CMD ["/usr/local/bin/python", "-m", "nir_myrmiaka"]

FROM prod as dev

# Install development dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install