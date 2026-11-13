from flask import Blueprint, current_app, jsonify

from dao.conexao import get_conexao

bp = Blueprint("sistema", __name__)


@bp.get("/api/saude")
def saude():
    """Confere se o sistema consegue falar com o banco de dados."""
    try:
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
        return jsonify({"status": "ok", "banco": "conectado"})
    except Exception as e:
        current_app.logger.error("Falha na conexão com o banco: %s", e)
        return jsonify({"status": "erro", "banco": "indisponível"}), 500
