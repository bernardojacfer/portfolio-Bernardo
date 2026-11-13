import json
import urllib.error
import urllib.parse
import urllib.request

from flask import Blueprint, current_app, jsonify, request

from config import SPORTSDB_KEY
from rotas.comum import erro

bp = Blueprint("times", __name__)

URL_SPORTSDB = "https://www.thesportsdb.com/api/v1/json/{chave}/searchteams.php"


@bp.get("/api/times")
def buscar_time():
    """Busca um time de futebol na TheSportsDB (a chamada é feita aqui, no servidor)."""
    nome = (request.args.get("nome") or "").strip()
    if not nome:
        return erro("Digite o nome de um time para buscar.", 400)

    url = URL_SPORTSDB.format(chave=urllib.parse.quote(SPORTSDB_KEY))
    url += "?" + urllib.parse.urlencode({"t": nome})
    pedido = urllib.request.Request(url, headers={"User-Agent": "portfolio-bernardo/1.0"})

    try:
        with urllib.request.urlopen(pedido, timeout=8) as resposta:
            dados = json.load(resposta)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        # URLError inclui HTTPError (ex.: 401 chave inválida, 429 limite de uso)
        current_app.logger.error("Falha ao consultar a TheSportsDB (%s): %s", url, e)
        return erro(
            "O serviço de times está indisponível no momento. Tente novamente em instantes.",
            502,
        )

    times = dados.get("teams") if isinstance(dados, dict) else None
    if not times:
        return erro(f'Não encontrei nenhum time chamado "{nome}". Tente outro nome.', 404)

    time = times[0]
    return jsonify({"time": {
        "nome": time.get("strTeam"),
        "pais": time.get("strCountry"),
        "liga": time.get("strLeague"),
        "estadio": time.get("strStadium"),
        "fundacao": time.get("intFormedYear"),
        "escudo": time.get("strBadge") or time.get("strTeamBadge"),
    }})
