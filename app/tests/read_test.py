import pytest
from app.tests.utilities import async_client, get_authorized_token


async def write_data(data: dict, headers):
    write_response = await async_client.post("/api/write",
                                             headers=headers,
                                             json=data,
                                             timeout=10)


@pytest.mark.asyncio
async def test_multiple_read_success():
    token = await get_authorized_token()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    data = {
        "data": {
            "success-multiple-read-key1": "value1",
            "success-multiple-read-key2": "value2",
            "success-multiple-read-key3": 1
        }
    }

    await write_data(data, headers)

    response = await async_client.post("/api/read", headers=headers, json={
        "keys": ["success-multiple-read-key1", "success-multiple-read-key2", "success-multiple-read-key3"]
    }, timeout=10)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    ans = response.json()
    assert ans["data"]["success-multiple-read-key1"] == "value1", "Failure writing first"
    assert ans["data"]["success-multiple-read-key2"] == "value2", "Failure writing second"
    assert ans["data"]["success-multiple-read-key3"] == 1, "Failure writing last"


@pytest.mark.asyncio
async def test_read_non_existent():
    token = await get_authorized_token()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = await async_client.post("/api/read",
                                       headers=headers,
                                       json={
                                           "keys": ["success-single-read-key1"]
                                       },
                                       timeout=10)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    ans = response.json()
    assert ans["data"]["success-single-read-key1"] is None, "Failure with non-existent value"
