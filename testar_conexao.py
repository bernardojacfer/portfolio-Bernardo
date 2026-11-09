"""Testa a conexão com o banco e mostra as tabelas existentes.

Uso:  python testar_conexao.py
"""
from dao.conexao import get_conexao


def main():
    with get_conexao() as con:
        cur = con.cursor()
        cur.execute("SELECT DATABASE()")
        print("Conectado ao banco:", cur.fetchone()[0])

        cur.execute("SHOW TABLES")
        tabelas = [linha[0] for linha in cur.fetchall()]
        print("Tabelas:", ", ".join(tabelas) if tabelas else "(nenhuma)")

        for tabela in tabelas:
            cur.execute(f"SELECT COUNT(*) FROM {tabela}")
            print(f"  {tabela}: {cur.fetchone()[0]} registro(s)")


if __name__ == "__main__":
    main()
