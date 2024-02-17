import asyncio
import random

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_307_TEMPORARY_REDIRECT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

pytestmark = pytest.mark.asyncio


class TestTransacoesRotas:
    cliente = random.randint(1, 5)

    async def test_rota_transacoes_404(self, client: AsyncClient) -> None:
        cliente = random.randint(6, 500)
        res = await client.post(
            f'/{cliente}/transacoes',
            json={'valor': 100, 'tipo': 'd', 'descricao': 'teste 404'},
        )

        assert res.status_code == HTTP_404_NOT_FOUND

    async def test_rota_transacoes_422(self, client: AsyncClient) -> None:
        cliente = random.randint(6, 500)
        res = await client.post(f'/{cliente}/transacoes')

        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    async def test_adicao_de_credito(self, client: AsyncClient) -> None:
        extrato = await client.get(f'/{self.cliente}/extrato')
        res = await client.post(
            f'/{self.cliente}/transacoes',
            json={
                'valor': abs(extrato.json()['saldo']['total']) + 1000,
                'tipo': 'c',
                'descricao': 'credito',
            },
        )

        assert res.status_code == HTTP_200_OK
        assert res.json()['saldo'] == 1000

    async def test_estourar_limite(self, client: AsyncClient) -> None:
        result = await client.post(
            f'/{self.cliente}/transacoes',
            json={'valor': 1000, 'tipo': 'd', 'descricao': 'zerar'},
        )
        limite = result.json()['limite']

        for descricao in range(11):
            res = await client.post(
                f'/{self.cliente}/transacoes',
                json={
                    'valor': limite / 10,
                    'tipo': 'd',
                    'descricao': str(descricao),
                },
            )

        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
