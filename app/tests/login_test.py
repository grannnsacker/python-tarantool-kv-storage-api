import pytest

from app.tests.utilities import async_client


@pytest.mark.asyncio
async def test_login_success():
    response = await async_client.post("/api/login", json={
        "username": "admin",
        "password": "presale"
    }, timeout=10)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    ans = response.json()
    assert "token" in ans.keys(), "No 'token' key in response"


@pytest.mark.asyncio
async def test_login_failure_username():
    response = await async_client.post("/api/login", json={
        "username": "fake_username",
        "password": "presale"
    }, timeout=10)

    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"
    ans = response.json()
    assert ans["detail"] == "Incorrect user data", "Failure response"


@pytest.mark.asyncio
async def test_login_failure_password():
    response = await async_client.post("/api/login", json={
        "username": "admin",
        "password": "fake_password"
    }, timeout=10)

    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"
    ans = response.json()
    assert ans["detail"] == "Incorrect user data", "Failure response"
