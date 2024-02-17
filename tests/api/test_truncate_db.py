import asyncpg
import pytest

from src.config import settings

pytestmark = pytest.mark.asyncio


class TestDB:
    async def test_truncate(self):
        query = """
            begin;
            update cliente set saldo = 0;
            truncate transacao restart identity;
            commit;
        """
        session = await asyncpg.create_pool(
            user=settings.pg_user,
            password=settings.pg_password,
            database=settings.pg_database,
            host=settings.pg_host,
            port=settings.pg_port,
            max_size=settings.pg_max_size,
            max_queries=settings.pg_max_queries,
        )
        await session.execute(query)
