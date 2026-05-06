# ⚡ FastAPI Layered Architecture Template

A modern, production-ready FastAPI template utilizing a clean, layered (hexagonal-style) architecture. This template is designed for building robust and scalable backend services with clear separation of concerns, easy testing, and high maintainability.

## 💡 Why This Template?

While FastAPI is incredibly fast and flexible, it doesn't enforce a specific project structure. As projects grow, they often turn into a tangled mess of tightly coupled route handlers, business logic, and database calls. This template provides **Enterprise-Grade Readiness** from minute zero.

- **Pre-Configured Tooling:** `uv`, `pytest`, `ruff`, and `alembic` are pre-integrated. No wrestling with environment setups.
- **Scalable Architecture:** Extends beyond simple MVC. It isolates API routing, business logic (Services), and database interactions (Repositories) making the app highly testable and maintainable.
- **Production-Ready Security & Observability:** JWT authentication, HttpOnly cookies for refresh tokens, token blacklisting, password hashing, and rate limiting are baked in. Out-of-the-box integration with Sentry for robust error monitoring.
- **Consistent Responses:** Global exception handlers utilizing centralized success and error messages prevent hardcoded strings and standardize the API response structures.
- **Docker First:** A `docker-compose.yaml` is ready to spin up your backend, PostgreSQL database, and Redis instances instantly.

---

## 🔗 Frontend Compatibility

This backend template is designed to seamlessly integrate with the companion **Next.js 16 + React 19 + TypeScript Enterprise Template**.
You can find the frontend template here: [kemalcalak/NextJS-Template](https://github.com/kemalcalak/NextJS-Template).

The two templates share the same auth contract: HttpOnly `access_token` / `refresh_token` cookies, `/api/v1` prefix, `X-Requested-With` CSRF header, and a uniform `{ success, data, message, error }` response envelope.

---

## 🚀 Features & Tech Stack

This template integrates the best-in-class Python ecosystem tools to provide a seamless developer experience:

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) for building APIs with Python 3.12+ based on standard Python type hints.
- **Architecture:** Strict Layered Architecture separating routers, services, repositories, use cases, and models, fully utilizing FastAPI's dependency injection.
- **Database & ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) with `asyncpg` for non-blocking operations, and [Alembic](https://alembic.sqlalchemy.org/) for schema migrations.
- **Observability & Error Tracking:** [Sentry](https://sentry.io/) built-in integration for tracking unhandled exceptions and performance tracing.
- **Caching:** [Redis](https://redis.io/) integration using `redis.asyncio` for robust, high-performance distributed caching.
- **Validation & Config:** [Pydantic v2](https://docs.pydantic.dev/latest/) and `pydantic-settings` for robust data validation and environment management.
- **Security & Auth:** JWT access/refresh tokens accepted via either HttpOnly cookies *or* `Authorization: Bearer`, `bcrypt` password hashing, **Redis-backed token blacklist** (logout invalidation), strict origin-check middleware (returns 404 for foreign origins), and [Slowapi](https://slowapi.readthedocs.io/en/latest/) rate limiting for brute-force protection.
- **Account Lifecycle:** Email verification, password reset, password change, and **soft-delete with grace period** — accounts marked for deletion can be reactivated until the cron worker purges them.
- **Background Jobs:** [arq](https://arq-docs.helpmanual.io/) worker (separate container in compose) runs cron jobs such as `delete_expired_accounts` at the configured time.
- **Audit Trail:** `user_activity` table records auth events and CRUD actions with IP / user agent. The `audit_unexpected_failure` decorator captures unexpected route failures.
- **Smart Email Validation & Delivery:** Built-in asynchronous email sending with SMTP, domain MX record checking using `dnspython`, and auto-updating disposable email provider filtering via Redis cache.
- **Standardized API Responses:** Global exception handlers standardizing success/error schemas, utilizing a centralized `messages` module (`app/core/messages/`) to prevent hardcoded responses.
- **First Superuser Seed:** On startup, an initial admin is created from `FIRST_SUPERUSER` / `FIRST_SUPERUSER_PASSWORD` if none exists.
- **Tooling:** [uv](https://docs.astral.sh/uv/) for blazing-fast package management, and [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- **Testing:** Comprehensive async testing setup with `pytest` and `pytest-asyncio`, in-memory SQLite via `aiosqlite`, `fakeredis`, and autouse SMTP/MX patches — tests never hit Postgres or the network.

---

## ✅ CI/CD Ready

The repository structure supports standard Continuous Integration pipelines out-of-the-box. Ensure you configure your CI (GitHub Actions, GitLab CI, etc.) to run:

1.  **Dependency Install:** `uv sync`
2.  **Linting:** `uv run ruff check .`
3.  **Formatting Check:** `uv run ruff format --check .`
4.  **Unit & Integration Tests:** `uv run pytest`

---

## 📦 Setup & Local Development

### Prerequisites

- Python >= 3.12
- Docker & Docker Compose (for local database and Redis)
- [`uv`](https://docs.astral.sh/uv/) package manager (recommended)

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/kemalcalak/fastapi-template.git
cd fastapi-template
```

### 2. Environment Variables

Create a `.env` file from the provided template:

```bash
cp .env.example .env
```

Your `.env` file should look like this, filled with your actual configuration:

```env
# Application Settings
PROJECT_NAME="FastAPI Template"
SECRET_KEY="changethis"
ENVIRONMENT="local"
FIRST_SUPERUSER="admin@example.com"
FIRST_SUPERUSER_PASSWORD="changethis"
FRONTEND_HOST="http://localhost:5173"

# Database Settings
POSTGRES_SERVER="localhost"
POSTGRES_PORT=5432
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="changethis"
POSTGRES_DB="app"

# Redis Cache Settings
REDIS_URL="redis://localhost:6379/0"

# Email / SMTP Settings (Optional)
SMTP_HOST="smtp.example.com"
SMTP_PORT=465
SMTP_USE_STARTTLS=True
SMTP_USE_SSL=False
SMTP_USER="smtp_username"
SMTP_PASSWORD="smtp_password"
EMAILS_FROM_EMAIL="noreply@example.com"

# Sentry (only initialized when ENVIRONMENT != "local")
SENTRY_DSN=
```

### 3. Start the Application via Docker

This project provides a `docker-compose.yaml` to spin up the entire stack, including the backend service, a local PostgreSQL instance, a Redis container, and the **arq background worker**:

```bash
docker-compose up -d --build
```

The API will be available at `http://localhost:8000`. You can test the endpoints via the Swagger UI available at `http://localhost:8000/docs`.

To run the worker manually (e.g. when developing the API on the host):

```bash
uv run arq app.worker.settings.WorkerSettings
```

### 4. Run Migrations

To generate and apply the database tables using Alembic, run the migration command inside the backend container:

```bash
# Apply existing migrations
docker-compose exec backend uv run alembic upgrade head
```

If you modify models in `app/models/` and need to generate a new migration script:

```bash
docker-compose exec backend uv run alembic revision --autogenerate -m "description_of_changes"
docker-compose exec backend uv run alembic upgrade head
```

---

## 🛠️ Testing & Code Quality

### Testing

Tests are written using `pytest` and configured for async execution with `pytest-asyncio`. Configuration details can be found in `pytest.ini`.

To run the test suite locally:

```bash
uv run pytest
```

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for both code linting and formatting. The configurations are specified in `pyproject.toml`.

- **Check for issues:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Auto-fix lint issues:** `uv run ruff check --fix .`

### Git Hooks (pre-commit)

The repo ships a `.pre-commit-config.yaml`. After cloning, install both hook stages once:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

**`pre-commit`** (~5–15 s) — runs on every `git commit` against staged files:

- `trim trailing whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`, `check-added-large-files`, `check-merge-conflict`, `detect-private-key`
- `ruff check --fix` (auto-fix lint)
- `ruff format`

**`pre-push`** (~30–60 s) — runs on every `git push`:

- `uv run pytest` — full test suite must pass before code leaves the machine.

To run all hooks manually against the whole repo: `uv run pre-commit run --all-files`.

### Metrics (Prometheus)

`prometheus-fastapi-instrumentator` collects metrics for every handled request. The `/metrics` endpoint (root path, **outside `/api/v1`**, hidden from Swagger) exposes them in the standard Prometheus exposition format. Default metrics: request count, latency histograms, in-progress requests, exceptions per handler, plus the standard Python runtime + process metrics. Health endpoints and `/metrics` itself are excluded from instrumentation to avoid noise.

**Auth model — three layers:**

1. **`include_in_schema=False`** — the endpoint is invisible in Swagger / OpenAPI.
2. **Environment-gated bearer token** — outside `ENVIRONMENT="local"`, the endpoint requires `Authorization: Bearer ${METRICS_TOKEN}`. Mismatched or missing tokens return **404** (not 401/403) so the endpoint's existence is not disclosed.
3. **`origin_check_middleware`** — browser cross-origin requests with a foreign `Origin` header are rejected by the global middleware, regardless of the token.

**Local dev — open access:**

```bash
curl http://localhost:8000/metrics
```

**Production / staging — bearer token required:**

```bash
# .env (or your secret store)
METRICS_TOKEN=$(openssl rand -hex 32)

# Prometheus scrape config (prometheus.yml)
scrape_configs:
  - job_name: fastapi
    authorization:
      type: Bearer
      credentials: <your METRICS_TOKEN>
    static_configs:
      - targets: ['api.example.com:8000']
```

> Even with the token, prefer to also restrict `/metrics` at the reverse proxy (Prometheus scraper IP allowlist or VPC-internal-only exposure). Defense-in-depth — the token is one layer, network policy is another.

---

## 📂 Project Structure

```bash
├── app/
│   ├── alembic/          # Alembic env + versions/ (generated migration scripts)
│   ├── api/              # API Layer: routers, deps.py, exception handlers, decorators
│   │   └── routes/
│   │       ├── auth.py, users.py, health.py
│   │       └── admin/    # Admin surface (gated by CurrentSuperUser)
│   ├── core/             # config, db, security, redis, rate_limit, email, messages/
│   ├── models/           # Domain Layer: SQLAlchemy ORM (User, UserActivity, …)
│   ├── repositories/     # Data Layer: async DB queries (no business rules)
│   ├── schemas/          # Pydantic v2 DTOs (Create / Update / Response per domain)
│   ├── services/         # Business Logic Layer: pure async functions, take AsyncSession
│   ├── use_cases/        # Cross-domain orchestration (e.g. activity logging)
│   ├── worker/           # arq worker — settings + cron jobs (e.g. account deletion)
│   ├── utils/            # Helper functions (datetime, email templates)
│   ├── tests/            # pytest suite (in-memory SQLite, fakeredis, mocked SMTP)
│   └── main.py           # FastAPI app, lifespan, CORS + origin middleware
├── alembic.ini           # Alembic settings
├── docker-compose.yaml   # Compose stack: backend + worker + db + redis
├── dockerfile            # Backend image (uv-based multi-stage build)
├── pyproject.toml        # Project dependencies and tool configurations
├── pytest.ini            # Pytest settings
└── uv.lock               # Dependency lock file (commit alongside dep changes)
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

> This project follows [Conventional Commits](https://www.conventionalcommits.org/).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See the `LICENSE` file at the root of the workspace for more information.
