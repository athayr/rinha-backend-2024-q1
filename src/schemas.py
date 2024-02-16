from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class TipoTransacao(StrEnum):
    credito = 'c'
    debito = 'd'


class LimiteSaldo(BaseModel):
    saldo: int
    limite: int


class TransacaoEntrada(BaseModel):
    valor: int = Field(default=1, ge=1)
    tipo: TipoTransacao
    descricao: str = Field(min_length=1, max_length=10)


class Transacao(TransacaoEntrada):
    realizada_em: datetime


class ExtratoSaldo(BaseModel):
    saldo: int = Field(serialization_alias='total')
    limite: int
    data_extrato: datetime = Field(default_factory=datetime.now)
