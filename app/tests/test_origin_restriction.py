import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_allowed_origin(client: AsyncClient):
    # Use an origin from settings.all_cors_origins
    # settings.all_cors_origins includes FRONTEND_HOST
    allowed_origin = settings.FRONTEND_HOST
    response = await client.get(
        "/users/me",  # Correct path
        headers={"Origin": allowed_origin},
    )
    # It should not be 404 due to origin (might be 401 if not logged in, but not 404)
    assert response.status_code != 404


@pytest.mark.asyncio
async def test_unauthorized_origin(client: AsyncClient):
    response = await client.get(
        "/auth/login",  # Use an endpoint that exists
        headers={"Origin": "http://malicious.com"},
    )
    assert response.status_code == 404
    assert response.json() == {"success": False, "error": "RESOURCE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_no_origin(client: AsyncClient):
    response = await client.get("/auth/login")
    # Should not be 404 due to missing origin
    assert response.status_code != 404
    # If /health doesn't exist, this might fail, but let's check a known endpoint
    pass
