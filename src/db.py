from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI

from src.config import settings


@asynccontextmanager
async def lifespan_database(app: FastAPI):
    app.state.connection_pool = await asyncpg.create_pool(
        user=settings.pg_user,
        password=settings.pg_password,
        database=settings.pg_database,
        host=settings.pg_host,
        port=settings.pg_port,
        max_size=settings.pg_max_size,
        max_queries=settings.pg_max_queries,
    )
    yield
    await app.state.connection_pool.close()
