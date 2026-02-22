# FastAPI Layered Architecture Template

A modern, production-ready FastAPI template utilizing a clean, layered (hexagonal-style) architecture. This template is designed for building robust and scalable backend services with clear separation of concerns, easy testing, and high maintainability.

## Features

- **Layered Architecture:** Strict separation between API logic, services, repositories, and data models.
- **Dependency Injection:** Fully utilizes FastAPI's dependency injection system.
- **Asynchronous Database:** `SQLModel` with `asyncpg` for non-blocking database operations.
- **Database Migrations:** Pre-configured `Alembic` for schema version control.
- **Authentication & Security:** JWT validation and secure password hashing using `bcrypt` and `python-jose`.
- **Environment Management:** Structured configuration via `pydantic-settings`.
- **Package Management via `uv`:** Extremely fast dependency resolution and environment management.
- **Testing:** Comprehensive test suite setup utilizing `pytest` and `pytest-asyncio`.
- **Code Quality:** `ruff` configuration for blazing-fast linting and formatting.
- **Docker Ready:** Includes `Dockerfile` and `docker-compose.yaml` for containerized deployments and local Postgres dev environment.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/)
- **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Driver:** `asyncpg` (for PostgreSQL)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/latest/)
- **Linter & Formatter:** [Ruff](https://docs.astral.sh/ruff/)
- **Testing:** `pytest` + `pytest-asyncio`
- **Error Tracking:** Sentry SDK
- **Package Manager:** `uv`

## Project Structure

```bash
├── app/
│   ├── alembic/          # Database migration configurations
│   ├── api/              # API Layer: FastAPI routers and route handlers
│   ├── core/             # Core configurations, security, exceptions, logging
│   ├── models/           # Domain Layer: SQLModel definitions
│   ├── repositories/     # Data Layer: Database operations and queries
│   ├── schemas/          # API Layer: Pydantic request/response schemas
│   ├── services/         # Business Logic Layer: Core use cases and orchestration
│   ├── tests/            # Test suite (integration and unit tests)
│   ├── utils/            # Helper functions and shared utilities
│   └── main.py           # Application entry point
├── alembic.ini           # Alembic settings
├── docker-compose.yaml   # Docker compose configuration (e.g., PostgreSQL DB)
├── Dockerfile            # Dockerfile for backend container
├── pyproject.toml        # Project dependencies and tool configurations
├── pytest.ini            # Pytest settings
└── uv.lock               # Dependency lock file
```

## Setup & Local Development

### Prerequisites

- Python >= 3.12
- Docker & Docker Compose (for local database)
- `uv` package manager (recommended)

### 1. Clone & Bootstrap

Clone the repository and install the dependencies. This project uses [uv](https://docs.astral.sh/uv/) for incredibly fast dependency management:

```bash
# Install uv if you haven't already
# pip install uv

# Install project dependencies
uv sync
```

### 2. Environment Variables

Create a `.env` file from the provided template:

```bash
cp .env.example .env
```
Ensure you set the correct database credentials inside `.env` (e.g., `DATABASE_URL`).

### 3. Start Local Database

This project provides a `docker-compose.yaml` to spin up a local PostgreSQL instance:

```bash
docker-compose up -d
```

### 4. Run Migrations

Generate and apply the tables using Alembic:

```bash
# Apply existing migrations
uv run alembic upgrade head
```

If you modify models in `app/models/` and need to generate a new migration script:

```bash
uv run alembic revision --autogenerate -m "description_of_changes"
uv run alembic upgrade head
```

### 5. Start the Application

Run the FastAPI development server:

```bash
# Using fastapi CLI standard
uv run fastapi dev app/main.py

# Alternatively via python with uvicorn (if installed explicitly)
uv run python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. You can test the endpoints via the Swagger UI available at `http://localhost:8000/docs`.

## Testing

Tests are written using `pytest` and configured for async execution with `pytest-asyncio`.

To run the test suite:

```bash
uv run pytest
```

Configuration details for `pytest` can be found in `pytest.ini`. 

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for both code linting and formatting. The configurations are specified in `pyproject.toml`.

To check formatting and lint files:
```bash
uv run ruff check .
```

To automatically format the code and fix auto-fixable lint issues:
```bash
uv run ruff format .
uv run ruff check --fix .
```
