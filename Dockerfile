FROM python:3.10-slim

ENV  PYTHONPATH: "/app"

WORKDIR /app

# Copy dependency files to create a cached layer for the packages
COPY pyproject.toml poetry.lock ./

# Install dependencies with poetry on global container interpreter
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

# Add entrypoint script to the container
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]