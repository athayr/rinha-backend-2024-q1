from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from starlette.responses import PlainTextResponse, RedirectResponse

from src.db import lifespan_database
from src.schemas import TransacaoEntrada
from src.service import extrato, nova_transacao

app: FastAPI = FastAPI(lifespan=lifespan_database)


@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url=app.docs_url)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse('', status_code=exc.status_code)


@app.post('/clientes/{cliente_id}/transacoes')
async def criar_nova_transacao(
    req: Request, cliente_id: int, transacao: TransacaoEntrada
):
    session = req.app.state.connection_pool
    return await nova_transacao(session, cliente_id, transacao)


@app.get('/clientes/{cliente_id}/extrato')
async def get_extrato(req: Request, cliente_id: int):
    return await extrato(req.app.state.connection_pool, cliente_id)
