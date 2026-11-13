"""Cria o banco e as tabelas executando o schema.sql.

Também atualiza uma tabela `usuarios` antiga (criada na fase PHP, com a coluna
`senha` e sem `perfil`), então pode ser executado de novo sem medo.

Uso:  python criar_banco.py
"""
from pathlib import Path

import mysql.connector

from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

SCHEMA = Path(__file__).parent / "schema.sql"


def comandos_sql(texto):
    """Separa o arquivo em comandos, ignorando linhas de comentário."""
    linhas = [l for l in texto.splitlines() if not l.strip().startswith("--")]
    return [c.strip() for c in "\n".join(linhas).split(";") if c.strip()]


def colunas(cur, tabela):
    cur.execute(
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
        (tabela,),
    )
    return {linha[0] for linha in cur.fetchall()}


def migrar_usuarios(cur):
    """Ajusta uma tabela `usuarios` criada antes da Etapa 2."""
    cols = colunas(cur, "usuarios")

    if "senha" in cols and "senha_hash" not in cols:
        cur.execute("ALTER TABLE usuarios CHANGE senha senha_hash VARCHAR(255) NOT NULL")
        print("Coluna `senha` renomeada para `senha_hash`.")

    if "perfil" not in cols:
        cur.execute(
            "ALTER TABLE usuarios ADD COLUMN perfil ENUM('admin', 'comum') "
            "NOT NULL DEFAULT 'comum' AFTER senha_hash"
        )
        print("Coluna `perfil` adicionada.")

    # Senhas gravadas pelo PHP (password_hash) usam outro formato e não funcionam no Flask.
    cur.execute("SELECT COUNT(*) FROM usuarios WHERE senha_hash LIKE '$2y$%'")
    antigos = cur.fetchone()[0]
    if antigos:
        print(
            f"ATENÇÃO: {antigos} usuário(s) da fase PHP não conseguem entrar no Flask "
            "(senha em outro formato). Apague-os ou cadastre-os de novo pelo site."
        )


def main():
    # Sem informar o banco: ele ainda pode não existir.
    con = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
    )
    try:
        cur = con.cursor()
        for comando in comandos_sql(SCHEMA.read_text(encoding="utf-8")):
            cur.execute(comando)
        migrar_usuarios(cur)
        con.commit()
        print("Banco e tabelas prontos.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
