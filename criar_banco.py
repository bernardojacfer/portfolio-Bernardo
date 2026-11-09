"""Cria o banco e as tabelas executando o schema.sql.

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


def main():
    # Sem informar o banco: ele ainda pode não existir.
    con = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
    )
    try:
        cur = con.cursor()
        for comando in comandos_sql(SCHEMA.read_text(encoding="utf-8")):
            cur.execute(comando)
        con.commit()
        print("Banco e tabelas criados com sucesso.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
