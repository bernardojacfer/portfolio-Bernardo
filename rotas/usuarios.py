import mysql.connector
from flask import Blueprint, g, jsonify, request

from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
from rotas.comum import (
    admin_obrigatorio, corpo_json, erro, login_obrigatorio, texto,
)

bp = Blueprint("usuarios", __name__)
dao = UsuarioDAO()

EMAIL_DUPLICADO = "Este e-mail já está cadastrado."


def _email_duplicado(excecao):
    # 1062 = entrada duplicada (chave UNIQUE do e-mail)
    return isinstance(excecao, mysql.connector.IntegrityError) and excecao.errno == 1062


@bp.post("/api/usuarios")
def criar():
    """Cadastro público. O primeiro cadastro sem nenhum admin no sistema vira admin."""
    dados = corpo_json()
    if dados is None:
        return erro("Envie os dados em JSON.", 400)

    senha = texto(dados, "senha")
    if "confirmar_senha" in dados and senha != texto(dados, "confirmar_senha"):
        return erro("As senhas não coincidem.", 400)

    try:
        usuario = Usuario(texto(dados, "nome"), texto(dados, "email"))
        usuario.definir_senha(senha)
    except ValueError as e:
        return erro(str(e), 400)

    if dao.buscar_por_email(usuario.email):
        return erro(EMAIL_DUPLICADO, 409)

    if dao.contar("admin") == 0:
        usuario.perfil = "admin"

    try:
        dao.inserir(usuario)
    except mysql.connector.Error as e:
        if _email_duplicado(e):
            return erro(EMAIL_DUPLICADO, 409)
        raise
    return jsonify({"usuario": usuario.to_dict()}), 201


@bp.get("/api/usuarios")
@admin_obrigatorio
def listar():
    busca = (request.args.get("busca") or "").strip()
    return jsonify({"usuarios": [u.to_dict() for u in dao.listar(busca or None)]})


@bp.get("/api/usuarios/<int:id>")
@login_obrigatorio
def buscar(id):
    if g.usuario.id != id and g.usuario.perfil != "admin":
        return erro("Você só pode ver o seu próprio perfil.", 403)
    usuario = dao.buscar_por_id(id)
    if usuario is None:
        return erro("Usuário não encontrado.", 404)
    return jsonify({"usuario": usuario.to_dict()})


@bp.put("/api/usuarios/<int:id>")
@login_obrigatorio
def atualizar(id):
    eh_admin = g.usuario.perfil == "admin"
    if g.usuario.id != id and not eh_admin:
        return erro("Você só pode editar o seu próprio perfil.", 403)

    dados = corpo_json()
    if dados is None:
        return erro("Envie os dados em JSON.", 400)

    usuario = dao.buscar_por_id(id)
    if usuario is None:
        return erro("Usuário não encontrado.", 404)

    # Perfil: só admin muda, e nunca o próprio (evita ficar sem administrador).
    perfil = dados.get("perfil", usuario.perfil)
    if perfil != usuario.perfil:
        if not eh_admin:
            return erro("Apenas administradores podem alterar o perfil.", 403)
        if g.usuario.id == id:
            return erro("Você não pode alterar o seu próprio perfil.", 403)
        if usuario.perfil == "admin" and dao.contar("admin") <= 1:
            return erro("O sistema precisa de pelo menos um administrador.", 409)

    try:
        usuario.nome = texto(dados, "nome")
        usuario.email = texto(dados, "email")
        usuario.perfil = perfil
        nova_senha = texto(dados, "senha")
        if nova_senha:
            usuario.definir_senha(nova_senha)
    except ValueError as e:
        return erro(str(e), 400)

    outro = dao.buscar_por_email(usuario.email)
    if outro and outro.id != id:
        return erro(EMAIL_DUPLICADO, 409)

    try:
        dao.atualizar(usuario)
    except mysql.connector.Error as e:
        if _email_duplicado(e):
            return erro(EMAIL_DUPLICADO, 409)
        raise
    return jsonify({"usuario": usuario.to_dict()})


@bp.delete("/api/usuarios/<int:id>")
@admin_obrigatorio
def excluir(id):
    if g.usuario.id == id:
        return erro("Você não pode excluir a sua própria conta.", 403)
    if not dao.excluir(id):
        return erro("Usuário não encontrado.", 404)
    return jsonify({"mensagem": "Usuário excluído."})
