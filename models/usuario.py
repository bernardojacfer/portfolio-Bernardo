from werkzeug.security import check_password_hash, generate_password_hash


class Usuario:
    """Representa um usuário do sistema (tabela `usuarios`)."""

    PERFIS = ("admin", "comum")

    def __init__(self, nome, email, senha_hash=None, perfil="comum",
                 id=None, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil
        self.criado_em = criado_em

    # ---- encapsulamento com validação ----
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        valor = (valor or "").strip()
        if not valor:
            raise ValueError("O nome é obrigatório.")
        if len(valor) > 100:
            raise ValueError("O nome deve ter no máximo 100 caracteres.")
        self._nome = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        valor = (valor or "").strip().lower()
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")
        if len(valor) > 150:
            raise ValueError("O e-mail deve ter no máximo 150 caracteres.")
        self._email = valor

    @property
    def perfil(self):
        return self._perfil

    @perfil.setter
    def perfil(self, valor):
        if valor not in self.PERFIS:
            raise ValueError("Perfil inválido.")
        self._perfil = valor

    # ---- comportamento ----
    def definir_senha(self, senha):
        if len(senha or "") < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        if not self.senha_hash:
            return False
        try:
            return check_password_hash(self.senha_hash, senha)
        except ValueError:
            # hash em formato desconhecido (ex.: gravado pelo PHP): não confere
            return False

    def to_dict(self):
        """Dados seguros para devolver em JSON (nunca inclui a senha)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil,
            "criado_em": str(self.criado_em) if self.criado_em else None,
        }
