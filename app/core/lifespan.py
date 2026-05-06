"""FastAPI lifespan: process-wide setup and teardown for shared resources."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.redis import close_redis, init_redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialise and dispose shared resources (Redis) for the API process."""
    await init_redis()
    try:
        yield
    finally:
        await close_redis()
