from dao.conexao import get_conexao
from models.mensagem import Mensagem

COLUNAS = "id, usuario_id, nome, email, mensagem, lida, criado_em"


def _montar(linha):
    return Mensagem(
        nome=linha["nome"],
        email=linha["email"],
        mensagem=linha["mensagem"],
        usuario_id=linha["usuario_id"],
        lida=bool(linha["lida"]),
        id=linha["id"],
        criado_em=linha["criado_em"],
    )


class MensagemDAO:
    """Acesso à tabela `mensagens`."""

    def inserir(self, m):
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO mensagens (usuario_id, nome, email, mensagem) "
                "VALUES (%s, %s, %s, %s)",
                (m.usuario_id, m.nome, m.email, m.mensagem),
            )
            con.commit()
            m.id = cur.lastrowid
            return cur.lastrowid

    def listar(self):
        with get_conexao() as con:
            cur = con.cursor(dictionary=True)
            cur.execute(f"SELECT {COLUNAS} FROM mensagens ORDER BY id DESC")
            return [_montar(l) for l in cur.fetchall()]

    def marcar_lida(self, id):
        """Marca como lida. Devolve True se a mensagem existe."""
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM mensagens WHERE id = %s", (id,))
            if cur.fetchone()[0] == 0:
                return False
            cur.execute("UPDATE mensagens SET lida = TRUE WHERE id = %s", (id,))
            con.commit()
            return True

    def excluir(self, id):
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM mensagens WHERE id = %s", (id,))
            con.commit()
            return cur.rowcount > 0
