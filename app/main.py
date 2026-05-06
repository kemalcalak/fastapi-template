from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.exception_handlers import (
    general_exception_handler,
    http_exception_handler,
    rate_limit_exception_handler,
    validation_exception_handler,
)
from app.api.main import api_router
from app.core.config import settings
from app.core.messages.error_message import ErrorMessages
from app.core.rate_limit import limiter
from app.core.redis import close_redis, init_redis


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate a stable operationId for OpenAPI clients.

    Falls back to the bare route name for routes without tags (e.g. the
    Prometheus /metrics endpoint registered by the instrumentator).
    """
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize and dispose shared resources (Redis) for the API process."""
    await init_redis()
    try:
        yield
    finally:
        await close_redis()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Exception Handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
app.state.limiter = limiter


@app.middleware("http")
async def origin_check_middleware(request: Request, call_next):
    """
    Strict origin check. Returns 404 for unauthorized origins.
    Allows same-origin requests (from the API's own origin).
    Hides error details and ensures always 404 for these cases.
    """
    origin = request.headers.get("origin")
    if origin:
        origin = origin.rstrip("/")

    # Allow same-origin requests
    if origin:
        # Reconstruct the request's own origin from scheme and host header
        scheme = request.url.scheme
        host = request.headers.get("host", "").rstrip("/")
        request_origin = f"{scheme}://{host}".rstrip("/")

        # Allow if origins match (same-origin request)
        if origin == request_origin:
            return await call_next(request)

    allowed_origins = settings.all_cors_origins

    if origin and allowed_origins and "*" not in allowed_origins:
        if origin not in allowed_origins:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": ErrorMessages.RESOURCE_NOT_FOUND},
            )
    return await call_next(request)


# Set all CORS enabled origins.
# allow_credentials + "*" is unsafe: some browsers honour it and would let any
# origin issue authenticated requests. Refuse that combination outright.
if settings.all_cors_origins:
    if "*" in settings.all_cors_origins:
        raise RuntimeError(
            "CORS misconfiguration: wildcard origin '*' cannot be combined "
            "with credentialed requests. Set explicit origins in "
            "BACKEND_CORS_ORIGINS / FRONTEND_HOST."
        )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Prometheus instrumentation — collect metrics for every handled request.
# Health and /metrics itself are excluded from instrumentation to keep noise
# out of the time series.
Instrumentator(
    excluded_handlers=["/metrics", f"{settings.API_V1_STR}/health/.*"],
).instrument(app)


@app.get("/metrics", include_in_schema=False)
async def metrics_endpoint(
    authorization: str | None = Header(default=None),
) -> Response:
    """Expose Prometheus metrics in the standard exposition format.

    Local dev keeps the endpoint open for convenience. In every other
    environment a bearer token (METRICS_TOKEN) is required; mismatched or
    missing tokens return 404 to avoid disclosing the endpoint to outsiders.
    """
    if settings.ENVIRONMENT != "local":
        expected = (
            f"Bearer {settings.METRICS_TOKEN}" if settings.METRICS_TOKEN else None
        )
        if expected is None or authorization != expected:
            raise HTTPException(
                status_code=404,
                detail=ErrorMessages.RESOURCE_NOT_FOUND,
            )
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
