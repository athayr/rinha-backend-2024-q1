from asyncpg import Pool, Record
from fastapi import status
from fastapi.exceptions import HTTPException

from src.queries import (
    GET_CLIENTE_IF_EXISTS,
    INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_C,
    INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_D,
    TRANSACOES_ROW,
)
from src.schemas import (
    ExtratoSaldo,
    LimiteSaldo,
    TipoTransacao,
    Transacao,
    TransacaoEntrada,
)


async def busca_cliente_por_id(session: Pool, id: int) -> Record:
    return await session.fetchrow(GET_CLIENTE_IF_EXISTS, id)


async def extrato(
    session: Pool, cliente_id: int
) -> dict[str, ExtratoSaldo | list[Transacao]]:

    saldo = await busca_cliente_por_id(session, cliente_id)

    if not saldo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    dados = await session.fetch(TRANSACOES_ROW, cliente_id)
    ultimas_transacoes = [Transacao(**transacao) for transacao in dados]

    return dict(
        saldo=ExtratoSaldo(**saldo),
        ultimas_transacoes=ultimas_transacoes,
    )


async def nova_transacao(
    session: Pool, cliente_id: int, transacao: TransacaoEntrada
) -> LimiteSaldo:
    cliente = await busca_cliente_por_id(session, cliente_id)

    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if (
        transacao.tipo == TipoTransacao.debito
        and abs(cliente['saldo']) + transacao.valor > cliente['limite']
    ):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    saldo = cliente['saldo']

    saldo += (
        transacao.valor
        if transacao.tipo == TipoTransacao.credito
        else -transacao.valor
    )

    query = (
        INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_D
        if transacao.tipo == TipoTransacao.debito
        else INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_C
    )

    await session.execute(query, cliente_id, *transacao.model_dump().values())

    return LimiteSaldo(saldo=saldo, limite=cliente['limite'])
