#!/bin/bash
set -e

cd /app

echo "Checking for existing migrations..."
if [ ! -d "app/migrations/versions" ] || [ -z "$(ls -A app/migrations/versions)" ]; then
    echo "No existing migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
else
    echo "Migrations directory exists."
fi

# Apply all migrations
echo "Applying database migrations..."
alembic upgrade head

# Continue with the default command (starting the application)
exec "$@"
