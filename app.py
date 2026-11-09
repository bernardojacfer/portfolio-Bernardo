from flask import Flask, jsonify

from config import SECRET_KEY
from dao.conexao import get_conexao

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.get("/api/saude")
def saude():
    """Confere se o sistema consegue falar com o banco de dados."""
    try:
        with get_conexao() as con:
            cur = con.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
        return jsonify({"status": "ok", "banco": "conectado"})
    except Exception as erro:
        app.logger.error("Falha na conexão com o banco: %s", erro)
        return jsonify({"status": "erro", "banco": "indisponível"}), 500


if __name__ == "__main__":
    app.run(debug=True)
