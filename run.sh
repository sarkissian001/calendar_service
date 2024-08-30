#!/bin/bash
set -e
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
    echo "calendar_api container is ready."
}


# Main script execution
main() {
    run_docker_compose
    wait_for_container
}

main
