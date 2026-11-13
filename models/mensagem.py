class Mensagem:
    """Mensagem enviada pelo formulário de contato (tabela `mensagens`)."""

    def __init__(self, nome, email, mensagem, usuario_id=None,
                 lida=False, id=None, criado_em=None):
        self.id = id
        self.usuario_id = usuario_id
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
        self.lida = lida
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
    def mensagem(self):
        return self._mensagem

    @mensagem.setter
    def mensagem(self, valor):
        valor = (valor or "").strip()
        if not valor:
            raise ValueError("A mensagem é obrigatória.")
        if len(valor) > 2000:
            raise ValueError("A mensagem deve ter no máximo 2000 caracteres.")
        self._mensagem = valor

    # ---- comportamento ----
    def marcar_como_lida(self):
        self.lida = True

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "nome": self.nome,
            "email": self.email,
            "mensagem": self.mensagem,
            "lida": bool(self.lida),
            "criado_em": str(self.criado_em) if self.criado_em else None,
        }
