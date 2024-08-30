#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 {create_migration|roll_back|apply_migrations} [comment]"
  exit 1
fi

COMMAND=$1
shift  # Remove the command from the args list

if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker first."
    exit 1
fi

CONTAINER_NAME="calendar_api"

case $COMMAND in
  create_migration)
    if [ -z "$1" ]; then
      echo "Provide a comment for the migration."
      exit 1
    fi
    COMMENT=$1
    echo "Creating a new migration with comment: $COMMENT"
    docker compose exec "$CONTAINER_NAME" bash -c "alembic revision --autogenerate -m '$COMMENT'"
    ;;

  roll_back)
    echo "Rolling back the last migration..."
    docker compose exec "$CONTAINER_NAME" bash -c "alembic downgrade -1"
    ;;

  apply_migrations)
    echo "Applying all pending migrations..."
    docker compose exec "$CONTAINER_NAME" bash -c "alembic upgrade head"
    ;;
  
  *)
    echo "Unknown command: $COMMAND"
    echo "Usage: $0 {create_migration|roll_back|apply_migrations} [comment]"
    exit 1
    ;;
esac
