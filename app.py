from pathlib import Path

import mysql.connector
from flask import Flask, abort, request, send_from_directory

from config import SECRET_KEY
from rotas import auth, mensagens, sistema, times, usuarios
from rotas.comum import erro

RAIZ = Path(__file__).resolve().parent

# static_folder=None: só servimos as pastas liberadas abaixo,
# nunca a raiz (que tem app.py, .env etc.).
app = Flask(__name__, static_folder=None)
app.secret_key = SECRET_KEY
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

if SECRET_KEY == "troque-esta-chave":
    app.logger.warning("SECRET_KEY padrão em uso: defina uma chave própria no arquivo .env.")

for modulo in (sistema, times, auth, usuarios, mensagens):
    app.register_blueprint(modulo.bp)


@app.after_request
def liberar_cors(resposta):
    """Só as rotas públicas e sem login podem ser chamadas de outra porta (Live Server)."""
    if request.path in ("/api/times", "/api/saude"):
        resposta.headers["Access-Control-Allow-Origin"] = "*"
    return resposta


# ---------------------------------------------------------------- erros em JSON
@app.errorhandler(mysql.connector.Error)
def erro_banco(e):
    app.logger.error("Erro no banco de dados: %s", e)
    return erro("Erro ao acessar o banco de dados. Tente novamente.", 500)


@app.errorhandler(404)
def nao_encontrado(e):
    if request.path.startswith("/api/"):
        return erro("Rota não encontrada.", 404)
    return "Página não encontrada.", 404


@app.errorhandler(405)
def metodo_nao_permitido(e):
    if request.path.startswith("/api/"):
        return erro("Método não permitido para esta rota.", 405)
    return "Método não permitido.", 405


# ---------------------------------------------------------------- site
@app.get("/")
@app.get("/index.html")
def home():
    return send_from_directory(RAIZ, "index.html")


@app.get("/pages/<path:nome>")
def pagina(nome):
    if not nome.endswith(".html"):  # os .php antigos não são servidos
        abort(404)
    return send_from_directory(RAIZ / "pages", nome)


@app.get("/css/<path:arquivo>")
@app.get("/js/<path:arquivo>")
@app.get("/img/<path:arquivo>")
def estatico(arquivo):
    pasta = request.path.split("/")[1]
    return send_from_directory(RAIZ / pasta, arquivo)


if __name__ == "__main__":
    app.run(debug=True)
