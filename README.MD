# Calendar API

This project is a simple calendar API service built using FastAPI, SQLAlchemy, and Alembic, with PostgreSQL as the database. The service allows users to create, update, delete, and retrieve calendar events. The project is containerised using Docker and managed with Docker Compose.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- **Docker**: Install Docker from [here](https://docs.docker.com/get-docker/).
- **Docker Compose**: Install Docker Compose from [here](https://docs.docker.com/compose/install/).

## Environment Variables

The project uses a `.env` file to manage environment-specific configurations. Ensure you have a `.env` file in the root directory of your project with the following variables:

```env
DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
DATABASE_NAME=<your_database_name>
DATABASE_PORT=5432
```

Replace the placeholders with actual values, there is also .env.example that you can use

## Run Application 

### 1. Clone the Repository


```bash
git clone https://github.com/your-username/calendar-api.git
cd calendar-api
```

### 2. Running the Service

To build and run the service using Docker Compose, execute the following script:

```bash
./run.sh
```

This script will:
- Build and start the Docker containers, including the PostgreSQL database and the Calendar API service.
- Wait for the `calendar_api` container to be ready as well as commit initial migrations.

The API service should run on `http://localhost:8000`, and PostgreSQL will be available on port `5432`.

you may also play with the swagger by visiting `http://localhost:8000/docs`

### 3. Applying Database Migrations

To apply database migrations, use the following command:

```bash
./migrate.sh apply_migrations
```

This will apply all pending migrations to ensure database schema is up to date.

### 4. Creating a New Migration

If schema changes a new migration can be created using the following command:

```bash
./migrate.sh create_migration "migration description"
```

This will generate a new migration script with the provided description.

### 5. Rolling Back the Last Migration

To roll back the last migration, use the following command:

```bash
./migrate.sh roll_back
```

This will undo the last applied migration.

## Project Structure

```
calendar-api/
│
├── Dockerfile                        # Dockerfile to build the calendar API container
├── README.MD                         # Project documentation
├── alembic.ini                       # Alembic configuration file
├── app                               # Main application directory
│   ├── __init__.py                   # Package initialization
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
│       ├── __init__.py               # Package initialization
│       └── test_main.py              # Tests for the main application
├── docker-compose.yml                # Docker Compose configuration file
├── entrypoint.sh                     # Entrypoint script for Docker containers
├── migrate.sh                        # Script to manage Alembic migrations
├── migrations                        # Alembic migration scripts
│   ├── README                        # Information about migrations
│   ├── env.py                        # Environment setup for Alembic
│   ├── script.py.mako                # Alembic migration script template
│   └── versions                      # Migration versions directory

├── poetry.lock                       # Poetry lock file for dependencies
├── pyproject.toml                    # Poetry project file
├── run.sh                            # Script to build and run the Docker containers
└── test_service.py                   # basic tests until proper tests are implemented

```

## API Documentation

Once the service is running, you can access the interactive API documentation provided by FastAPI:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## TODO

Here are some tasks that should be completed to enhance the project:

- **Testing**:
  - Create unit tests for the CRUD operations.
  - Create integration tests for the API endpoints.
  - Set up a CI/CD pipeline to run tests automatically.
  
- **Postman Collection**:
  - Create a Postman collection to test the API endpoints.
  - Include the collection in the repository for easy access.
  
- **Environment Configuration**:
  - Ensure the `.env` file is properly configured for different environments (e.g., development, production).
  - Add environment-specific configuration files if needed.

- **Security**:
  - Implement authentication and authorization for the API endpoints.

