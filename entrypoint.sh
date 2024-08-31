#!/bin/bash
set -e

cd /app

## Apply all migrations
#echo "Applying database migrations..."
#alembic upgrade head

# Continue with the default command (starting the application)
exec "$@"
