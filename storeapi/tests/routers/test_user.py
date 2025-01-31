import pytest
from httpx import AsyncClient


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(url="/register", json={"email": email, "password": password})


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "test261027@example.net", "1234")
    # Print or log the response content for debugging
    print(response.json())
    assert response.status_code == 201
    assert "User created" in response.json()["detail"]


@pytest.mark.anyio
async def test_register_user_already_exists(async_client: AsyncClient, registered_user: dict):
    response = await register_user(async_client, registered_user["email"], registered_user["password"])
    assert response.status_code == 400
    assert "already exist" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/token", json={"email": "test@example1.net", "password": "1234"}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_user(async_client: AsyncClient, registered_user: dict):
    response = await async_client.post(
        "/token",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        },
    )
    assert response.status_code == 200
