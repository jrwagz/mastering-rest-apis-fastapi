from typing import AsyncGenerator

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
import pytest

from socialapi.main import app
from socialapi.routers.post import comment_table, post_table


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client() -> AsyncGenerator:
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://testserver") as ac:
            yield ac
