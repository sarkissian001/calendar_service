#!/bin/bash
set -e


SERVICE_NAME="calendar_api"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)



# Function to build and run Docker Compose
run_docker_compose() {
    echo "Building and starting Docker containers..."
    docker compose down && docker compose up --build -d
    echo "Docker containers are up and running."
}

# Function to wait for the calendar_api container to be ready
wait_for_container() {
    echo "Waiting for calendar_api container to be ready..."
    until docker compose exec calendar_api bash -c "echo 'Container is ready'"; do
        sleep 1
    done
    echo "$SERVICE_NAME container is ready."
}

check_and_create_initial_migration() {
    MIGRATIONS_DIR="$SCRIPT_DIR/migrations/versions"

    # Check if there are no .py files in the directory
    if ! ls "$MIGRATIONS_DIR"/*.py 1> /dev/null 2>&1; then
        echo "No initial migrations found; creating ..."
        docker compose exec $SERVICE_NAME bash -c "alembic revision --autogenerate -m 'initial_migration' && alembic upgrade head"

        echo "Initial migration setup (if needed) is complete."
    else
         echo "There are already existing migrations - applying...."
         docker compose exec $SERVICE_NAME bash -c "alembic upgrade head"
    fi
}


main() {
    run_docker_compose
    wait_for_container
    check_and_create_initial_migration
}

main
