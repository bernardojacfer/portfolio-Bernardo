from flask import Blueprint, jsonify

from dao.mensagem_dao import MensagemDAO
from models.mensagem import Mensagem
from rotas.comum import admin_obrigatorio, corpo_json, erro, texto, usuario_logado

bp = Blueprint("mensagens", __name__)
dao = MensagemDAO()


@bp.post("/api/mensagens")
def enviar():
    """Formulário de contato: qualquer visitante pode enviar."""
    dados = corpo_json()
    if dados is None:
        return erro("Envie os dados em JSON.", 400)

    try:
        mensagem = Mensagem(
            texto(dados, "nome"), texto(dados, "email"), texto(dados, "mensagem")
        )
    except ValueError as e:
        return erro(str(e), 400)

    # Se quem enviou está logado, a mensagem fica ligada ao usuário.
    autor = usuario_logado()
    mensagem.usuario_id = autor.id if autor else None

    dao.inserir(mensagem)
    return jsonify({"mensagem": mensagem.to_dict()}), 201


@bp.get("/api/mensagens")
@admin_obrigatorio
def listar():
    return jsonify({"mensagens": [m.to_dict() for m in dao.listar()]})


@bp.patch("/api/mensagens/<int:id>/lida")
@admin_obrigatorio
def marcar_lida(id):
    if not dao.marcar_lida(id):
        return erro("Mensagem não encontrada.", 404)
    return jsonify({"mensagem": "Mensagem marcada como lida."})


@bp.delete("/api/mensagens/<int:id>")
@admin_obrigatorio
def excluir(id):
    if not dao.excluir(id):
        return erro("Mensagem não encontrada.", 404)
    return jsonify({"mensagem": "Mensagem excluída."})
