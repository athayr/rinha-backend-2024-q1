import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import app as app_client

fake = Faker('pt_BR')


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app() -> FastAPI:
    return app_client


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver/clientes',
            headers={'Content-Type': 'application/json'},
        ) as client:
            yield client
