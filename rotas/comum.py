"""Funções compartilhadas pelas rotas: respostas de erro, leitura do JSON e permissões."""
from functools import wraps

from flask import g, jsonify, request, session

from dao.usuario_dao import UsuarioDAO


def erro(mensagem, status):
    return jsonify({"erro": mensagem}), status


def corpo_json():
    """Devolve o JSON enviado pelo front-end, ou None se não for um objeto JSON."""
    dados = request.get_json(silent=True)
    return dados if isinstance(dados, dict) else None


def texto(dados, campo):
    """Lê um campo como texto (qualquer outro tipo vira string vazia)."""
    valor = dados.get(campo)
    return valor if isinstance(valor, str) else ""


def usuario_logado():
    """Usuário da sessão atual (ou None). Se ele foi apagado, encerra a sessão."""
    id_usuario = session.get("usuario_id")
    if not id_usuario:
        return None
    usuario = UsuarioDAO().buscar_por_id(id_usuario)
    if usuario is None:
        session.clear()
    return usuario


def login_obrigatorio(funcao):
    @wraps(funcao)
    def interna(*args, **kwargs):
        usuario = usuario_logado()
        if usuario is None:
            return erro("Faça login para continuar.", 401)
        g.usuario = usuario
        return funcao(*args, **kwargs)
    return interna


def admin_obrigatorio(funcao):
    @wraps(funcao)
    @login_obrigatorio
    def interna(*args, **kwargs):
        if g.usuario.perfil != "admin":
            return erro("Apenas administradores podem fazer isso.", 403)
        return funcao(*args, **kwargs)
    return interna
