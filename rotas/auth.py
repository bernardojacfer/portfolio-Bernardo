from flask import Blueprint, g, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash

from dao.usuario_dao import UsuarioDAO
from rotas.comum import corpo_json, erro, login_obrigatorio, texto

bp = Blueprint("auth", __name__)

# Usado quando o e-mail não existe, para o tempo de resposta não revelar se a conta existe.
HASH_FALSO = generate_password_hash("senha-falsa")


@bp.post("/api/login")
def login():
    dados = corpo_json()
    if dados is None:
        return erro("Envie os dados em JSON.", 400)

    email = texto(dados, "email").strip().lower()
    senha = texto(dados, "senha")
    if not email or not senha:
        return erro("Informe e-mail e senha.", 400)

    usuario = UsuarioDAO().buscar_por_email(email)
    if usuario is None:
        check_password_hash(HASH_FALSO, senha)
        return erro("E-mail ou senha inválidos.", 401)
    if not usuario.verificar_senha(senha):
        return erro("E-mail ou senha inválidos.", 401)

    session.clear()
    session["usuario_id"] = usuario.id
    return jsonify({"usuario": usuario.to_dict()})


@bp.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada."})


@bp.get("/api/me")
@login_obrigatorio
def me():
    return jsonify({"usuario": g.usuario.to_dict()})
