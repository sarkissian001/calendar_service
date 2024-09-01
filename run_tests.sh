#!/bin/bash
set -e

SERVICE_NAME="calendar_api"

# Check if the service container is running
if [ "$(docker compose ps -q $SERVICE_NAME)" ]; then
    echo "Running tests inside the Docker Compose service: $SERVICE_NAME"
    docker compose exec $SERVICE_NAME bash -c "pytest app/tests"
else
    echo "Service $SERVICE_NAME is not running"
    exit 1
fi