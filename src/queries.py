GET_CLIENTE_IF_EXISTS = 'SELECT saldo, limite FROM cliente WHERE id = $1;'

INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_D = """
WITH atualiza_saldo AS (
    UPDATE cliente
    SET saldo = saldo - $2
    WHERE id = $1 and limite + saldo >= $2
    RETURNING saldo, limite > 0 as limite, id
)
INSERT INTO
transacao (valor, tipo, descricao, cliente_id)
SELECT
    $2, $3, $4, atualiza_saldo.id
FROM atualiza_saldo
WHERE limite
RETURNING valor
"""

INSERT_TRANSACAO_E_UPDATE_SALDO_TIPO_C = """
WITH atualiza_saldo AS (
    UPDATE cliente
    SET saldo = saldo + $2
    WHERE id = $1
    RETURNING saldo, limite > 0 as limite, id
)
INSERT INTO
transacao (valor, tipo, descricao, cliente_id)
SELECT
    $2, $3, $4, atualiza_saldo.id
FROM atualiza_saldo
WHERE limite
RETURNING valor
"""

TRANSACOES_ROW = """
    SELECT
        id,
        valor,
        tipo,
        descricao,
        cliente_id,
        realizada_em
    FROM transacao
    WHERE cliente_id = $1
    ORDER BY realizada_em DESC
    LIMIT 10
"""
