from dao.conexao import get_conexao
from models.usuario import Usuario

COLUNAS = "id, nome, email, senha_hash, perfil, criado_em"


def _montar(linha):
    """Transforma uma linha do banco em um objeto Usuario."""
    return Usuario(
        nome=linha["nome"],
        email=linha["email"],
        senha_hash=linha["senha_hash"],
        perfil=linha["perfil"],
        id=linha["id"],
        criado_em=linha["criado_em"],
    )


class UsuarioDAO:
    """Acesso à tabela `usuarios`. Todas as consultas usam parâmetros (%s)."""

    def inserir(self, usuario):
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, perfil) "
                "VALUES (%s, %s, %s, %s)",
                (usuario.nome, usuario.email, usuario.senha_hash, usuario.perfil),
            )
            con.commit()
            usuario.id = cur.lastrowid
            return cur.lastrowid

    def listar(self, busca=None):
        sql = f"SELECT {COLUNAS} FROM usuarios"
        parametros = ()
        if busca:
            sql += " WHERE nome LIKE %s OR email LIKE %s"
            parametros = (f"%{busca}%", f"%{busca}%")
        sql += " ORDER BY id DESC"
        with get_conexao() as con:
            cur = con.cursor(dictionary=True)
            cur.execute(sql, parametros)
            return [_montar(l) for l in cur.fetchall()]

    def buscar_por_id(self, id):
        with get_conexao() as con:
            cur = con.cursor(dictionary=True)
            cur.execute(f"SELECT {COLUNAS} FROM usuarios WHERE id = %s", (id,))
            linha = cur.fetchone()
            return _montar(linha) if linha else None

    def buscar_por_email(self, email):
        with get_conexao() as con:
            cur = con.cursor(dictionary=True)
            cur.execute(f"SELECT {COLUNAS} FROM usuarios WHERE email = %s", (email,))
            linha = cur.fetchone()
            return _montar(linha) if linha else None

    def atualizar(self, usuario):
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE usuarios SET nome = %s, email = %s, senha_hash = %s, perfil = %s "
                "WHERE id = %s",
                (usuario.nome, usuario.email, usuario.senha_hash, usuario.perfil, usuario.id),
            )
            con.commit()

    def excluir(self, id):
        """Apaga o usuário. Devolve True se existia."""
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            con.commit()
            return cur.rowcount > 0

    def contar(self, perfil=None):
        """Conta usuários; com `perfil`, conta só os daquele perfil."""
        sql = "SELECT COUNT(*) FROM usuarios"
        parametros = ()
        if perfil:
            sql += " WHERE perfil = %s"
            parametros = (perfil,)
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute(sql, parametros)
            return cur.fetchone()[0]
