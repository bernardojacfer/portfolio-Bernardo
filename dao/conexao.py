"""Conexão com o MySQL, usada por todos os DAOs."""
from contextlib import contextmanager

import mysql.connector

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


@contextmanager
def get_conexao():
    """Abre uma conexão e garante que ela seja fechada ao sair do `with`.

    Uso:
        with get_conexao() as con:
            cur = con.cursor()
            ...
    """
    con = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )
    try:
        yield con
    finally:
        con.close()
