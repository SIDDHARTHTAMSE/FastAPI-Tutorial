from typing import AsyncGenerator, Generator
import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from storeapi.main import post_table, comment_table

os.environ["ENV_STATE"] = "test" #

from storeapi.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
