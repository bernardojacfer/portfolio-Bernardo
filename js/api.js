// Funções usadas por todas as páginas para conversar com a API Flask via Fetch.

// Chama uma rota da API e devolve o JSON. Em caso de erro, lança um Error com a
// mensagem que veio do servidor (ex.: "E-mail ou senha inválidos.").
async function api(url, { metodo = "GET", corpo } = {}) {
  const config = { method: metodo, headers: {}, credentials: "same-origin" };
  if (corpo !== undefined) {
    config.headers["Content-Type"] = "application/json";
    config.body = JSON.stringify(corpo);
  }

  let resposta;
  try {
    resposta = await fetch(url, config);
  } catch (e) {
    throw new Error(
      "Não foi possível falar com o servidor. Confira se o Flask está rodando (python app.py)."
    );
  }

  let dados = {};
  try {
    dados = await resposta.json();
  } catch (e) {
    // resposta sem JSON: segue com a mensagem genérica abaixo
  }

  if (!resposta.ok) {
    const erro = new Error(dados.erro || `Erro ${resposta.status}.`);
    erro.status = resposta.status;
    throw erro;
  }
  return dados;
}

// Mostra (ou limpa) um aviso. tipo: "erro" ou "sucesso". Sem texto, esconde o aviso.
function mostrarMensagem(elemento, texto, tipo) {
  elemento.textContent = texto || "";
  elemento.className = texto ? `mensagem ${tipo}` : "mensagem";
  elemento.hidden = !texto;
}

// Cria um elemento só com texto (textContent: evita injeção de HTML).
function criar(tag, texto, classe) {
  const elemento = document.createElement(tag);
  if (texto !== undefined && texto !== null) elemento.textContent = texto;
  if (classe) elemento.className = classe;
  return elemento;
}

// "2026-11-12 20:22:45" -> "12/11/2026 20:22"
function formatarData(texto) {
  if (!texto) return "";
  const data = new Date(texto.replace(" ", "T"));
  if (isNaN(data)) return texto;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// Garante que há alguém logado (e, se pedido, que é administrador).
// Sem login, manda para a tela de login e devolve null.
async function exigirLogin({ admin = false } = {}) {
  try {
    const { usuario } = await api("/api/me");
    if (admin && usuario.perfil !== "admin") {
      window.location.href = "/pages/dashboard.html";
      return null;
    }
    return usuario;
  } catch (erro) {
    if (erro.status === 401) {
      window.location.href = "/pages/login.html";
      return null;
    }
    throw erro;
  }
}
