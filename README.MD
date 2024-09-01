# Calendar API

This project is a simple calendar API service built using FastAPI, SQLAlchemy, and Alembic, with PostgreSQL as the database. The service allows users to create, update, delete, and retrieve calendar events. The project is containerised using Docker and managed with Docker Compose.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- **Docker**: Install Docker from [here](https://docs.docker.com/get-docker/).
- **Docker Compose**: Install Docker Compose from [here](https://docs.docker.com/compose/install/).
- **Python 3.12+**: Ensure you have Python version 3.12 or above installed. You can download Python from [here](https://www.python.org/downloads/).
- **Poetry**: Poetry is used for dependency management and packaging in this project. Install Poetry from [here](https://python-poetry.org/docs/#installation).


### Note: 
You need poetry and Python to be installed for local development but otherwise you can skip this part


## Environment Variables

The project uses a `.env` file to manage environment-specific configurations. Ensure you have a `.env` file in the root directory of your project with the following variables:

```env
DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
DATABASE_NAME=<your_database_name>
DATABASE_PORT=5432
```

Replace the placeholders with your actual values. You can also use [.env.example](.env.example) to guide you

## Getting Started

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone git@github.com:sarkissian001/calendar_service.git
cd calendar-api
```

### 2. Installing Dependencies

To install the dependencies using Poetry, run:

```bash
poetry install
```

This will create a virtual environment and install all required packages.

### 3. Running the Service

To build and run the service using Docker Compose, execute the following script:

```bash
./run.sh
```

This script will:
- Build and start the Docker containers, including the PostgreSQL database and the Calendar API service.
- Wait for the `calendar_api` container to be ready.

The API service should now be running on `http://localhost:8000`, and PostgreSQL will be available on port `5432`.

### 4. Running Tests

You have multiple options to run the tests:

- **Option 1: Run tests using Poetry directly**:

  ```bash
  poetry run pytest app/tests
  ```

- **Option 2: Activate the Poetry shell and run tests**:

  ```bash
  poetry shell
  pytest app/tests
  ```

- **Option 3: Run tests inside the Docker container**:

  You can also run the tests inside the Docker container by executing the `run_tests.sh` script:

  ```bash
  ./run_tests.sh
  ```

  This script will execute `docker compose exec` to run `pytest app/tests` inside the `calendar_service` container.

### 5. Applying Database Migrations

To apply database migrations, use the following command:

```bash
./migrate.sh apply_migrations
```

This will apply all pending migrations to ensure your database schema is up to date.

### 6. Creating a New Migration

If you need to create a new migration, use the following command:

```bash
./migrate.sh create_migration "Your migration description"
```

This will generate a new migration script with the provided description.

### 7. Rolling Back the Last Migration

If you need to roll back the last migration, use the following command:

```bash
./migrate.sh roll_back
```

This will undo the last applied migration.

## Project Structure

```
.
├── Dockerfile                        # Dockerfile to build the calendar API container
├── README.MD                         # Project documentation
├── alembic.ini                       # Alembic configuration file
├── app                               # Main application directory
│   ├── __init__.py                   # Package initialisation
│   ├── crud.py                       # CRUD operations
│   ├── database                      # Database-related configurations
│   │   ├── connection.py             # Database connection setup
│   │   └── database_config.py        # Database configuration settings
│   ├── main.py                       # FastAPI entry point
│   ├── models                        # SQLAlchemy models
│   │   └── event_models.py           # Event model definition
│   ├── routes                        # API route definitions
│   │   ├── __init__.py               # Package initialization
│   │   └── events.py                 # Event-related API routes
│   ├── schemas                       # Pydantic models (schemas)
│   │   └── event_schema.py           # Event schema definition
│   └── tests                         # Test cases
│       ├── __init__.py               # Package initialisation
│       ├── conftest.py               # Pytest fixture configurations
│       ├── test_events.py            # Tests for event-related functionalities
│       └── test_main.py              # Tests for the main application
├── docker-compose.yml                # Docker Compose configuration file
├── entrypoint.sh                     # Entrypoint script for Docker containers
├── migrate.sh                        # Script to manage Alembic migrations
├── migrations                        # Alembic migration scripts
│   ├── README                        # Information about migrations
│   ├── env.py                        # Environment setup for Alembic
│   ├── script.py.mako                # Alembic migration script template
│   └── versions                      # Migration versions directory
│       └── 8b28d8428e05_initial_migration.py  # Example migration script
├── poetry.lock                       # Poetry lock file for dependencies
├── pyproject.toml                    # Poetry project file
├── pytest.ini                        # Pytest configuration file
├── run.sh                            # Script to build and run the Docker containers
├── run_tests.sh                      # Script to run tests inside the Docker container
└── test_service.py                   # Additional test scripts
```

## API Documentation

Once the service is running, you can access the interactive API documentation provided by FastAPI:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## TODO

Here are some tasks that should be completed to enhance the project:

- **Testing**:
  - Create additional unit tests for the CRUD operations.
  - Set up a CI/CD pipeline to run tests automatically.
  
- **Postman Collection**:
  - Create a Postman collection to test the API endpoints.
  - Include the collection in the repository for easy access.
  
- **Environment Configuration**:
  - Ensure the `.env` file is properly configured for different environments (e.g., development, production).
  - Add environment-specific configuration files if needed.

- **Error Handling**:
  - Improve error handling and validation in the API endpoints.
  - Create custom error messages for common issues (e.g., missing required fields, invalid data).

- **Logging**:
  - Implement logging to capture important events and errors.
  - Configure logging to output to both console and file.

- **Security**:
  - Implement authentication and authorization for the API endpoints.
  - Consider using OAuth2 or JWT for securing the API.

