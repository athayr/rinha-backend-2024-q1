import asyncio
import random

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_307_TEMPORARY_REDIRECT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_429_TOO_MANY_REQUESTS,
)

pytestmark = pytest.mark.asyncio


class TestExtratoRotas:
    async def test_rota_extrato_404(self, client: AsyncClient) -> None:
        res = await client.get('/6/extrato')

        assert res.status_code == HTTP_404_NOT_FOUND

    async def test_cliente_sem_dado(self, client: AsyncClient) -> None:
        cliente = random.randint(1, 5)
        res = await client.get(f'/{cliente}/extrato')

        assert res.status_code == HTTP_200_OK
        assert res.json()['ultimas_transacoes'] == []
        assert res.json()['saldo']['total'] == 0

    async def test_cliente_com_dado(self, client: AsyncClient) -> None:
        cliente = random.randint(1, 5)
        extrato = await client.get(f'/{cliente}/extrato')

        for descricao in range(12):
            await client.post(
                f'/{cliente}/transacoes',
                json={'valor': 100, 'tipo': 'd', 'descricao': str(descricao)},
            )

        res = await client.get(f'/{cliente}/extrato')

        assert res.status_code == HTTP_200_OK
        assert len(res.json()['ultimas_transacoes']) == 10
        assert res.json()['saldo']['total'] == -1200
