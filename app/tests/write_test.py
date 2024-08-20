import pytest
from app.tests.utilities import async_client, get_authorized_token


async def read_data(data, headers):
    read_response = await async_client.post("/api/read",
                                            headers=headers,
                                            json=data,
                                            timeout=10)

    return read_response.json(), read_response.status_code


@pytest.mark.asyncio
async def test_multiple_write_success():
    token = await get_authorized_token()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    write_response = await async_client.post("/api/write", headers=headers, json={
        "data": {
            "success-multiple-write-key1": "value1",
            "success-multiple-write-key2": "value2",
            "success-multiple-write-key3": 1
        }
    }, timeout=10)
    assert write_response.status_code == 200, f"Expected status code 200, got {write_response.status_code}"
    write_ans = write_response.json()
    assert write_ans["status"] == "success", "Failure response"

    data = {"keys": [
        "success-multiple-write-key1",
        "success-multiple-write-key2",
        "success-multiple-write-key3"
    ]}
    read_ans, status_code = await read_data(data, headers)
    assert read_ans["data"]["success-multiple-write-key1"] == "value1", "Failure multiple writing first"
    assert read_ans["data"]["success-multiple-write-key2"] == "value2", "Failure multiple writing second"
    assert read_ans["data"]["success-multiple-write-key3"] == 1, "Failure multiple writing last"
    assert write_response.status_code == 200, f"Expected status code 200, got {write_response.status_code}"


@pytest.mark.asyncio
async def test_single_write_success():
    token = await get_authorized_token()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    write_response = await async_client.post("/api/write", headers=headers, json={
        "data": {
            "success-single-write-key1": "value1"
        }
    }, timeout=10)

    assert write_response.status_code == 200, f"Expected status code 200, got {write_response.status_code}"
    write_ans = write_response.json()
    assert write_ans["status"] == "success", "Failure response"

    data = {"keys": [
        "success-single-write-key1"
    ]}
    read_ans, status_code = await read_data(data, headers)
    assert read_ans["data"]["success-single-write-key1"] == "value1", "Failure writing single"
    assert status_code == 200, f"Expected status code 200, got {write_response.status_code}"


@pytest.mark.asyncio
async def test_writing_failure():
    token = await get_authorized_token()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = await async_client.post("/api/write", headers=headers, json={
        "data": {
            "failure-multiple-writing-key1": [1, 2]
        }
    }, timeout=10)

    assert response.status_code == 422, f"Expected status code 422, got {response.status_code}"
