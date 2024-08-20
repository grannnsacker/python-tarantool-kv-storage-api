from httpx import AsyncClient, ASGITransport

from app.main import app
from app.repositories import get_connection_repository


async def get_test_connection_repository():
    test_connection_repository = await get_connection_repository()
    await test_connection_repository.get_connection()
    try:
        yield test_connection_repository
    finally:
        await test_connection_repository.discard_connection()


async def get_authorized_token():
    response = await async_client.post("/api/login", json={
            "username": "admin",
            "password": "presale"
    }, timeout=10)

    ans = response.json()
    return ans["token"]

app.dependency_overrides[get_connection_repository] = get_test_connection_repository

async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")