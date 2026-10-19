// Busca informações de um time de futebol na API pública TheSportsDB
// e mostra o resultado na página sem recarregar.
const URL_API = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php";

async function buscarTime(nome) {
  const resultado = document.getElementById("time-resultado");
  const termo = nome.trim();

  // Cenário inválido 1: campo vazio (nem chama a API)
  if (termo === "") {
    resultado.className = "feedback error";
    resultado.textContent = "Digite o nome de um time para buscar.";
    return;
  }

  resultado.className = "feedback";
  resultado.textContent = "Buscando...";

  try {
    const resposta = await fetch(`${URL_API}?t=${encodeURIComponent(termo)}`);

    if (!resposta.ok) {
      throw new Error(`Erro HTTP ${resposta.status}`);
    }

    const dados = await resposta.json();

    // Cenário inválido 2: a API responde, mas não existe time com esse nome
    if (!dados.teams) {
      resultado.className = "feedback error";
      resultado.textContent = `Não encontrei nenhum time chamado "${termo}". Tente outro nome.`;
      return;
    }

    // Cenário válido: monta o cartão com os dados do JSON
    mostrarTime(dados.teams[0]);
  } catch (erro) {
    // Falha de rede, API fora do ar etc.
    console.error("Falha na requisição:", erro);
    resultado.className = "feedback error";
    resultado.textContent =
      "Não foi possível buscar o time agora. Verifique sua conexão e tente novamente.";
  }
}

function mostrarTime(time) {
  const resultado = document.getElementById("time-resultado");
  resultado.className = "";
  resultado.innerHTML = "";

  const cartao = document.createElement("div");
  cartao.className = "card time-card";

  const escudo = time.strBadge || time.strTeamBadge;
  if (escudo) {
    const img = document.createElement("img");
    img.src = escudo;
    img.alt = `Escudo do ${time.strTeam}`;
    img.className = "time-escudo";
    cartao.appendChild(img);
  }

  const titulo = document.createElement("h2");
  titulo.textContent = time.strTeam;
  cartao.appendChild(titulo);

  const linhas = [
    `País: ${time.strCountry || "não informado"}`,
    `Liga: ${time.strLeague || "não informada"}`,
    `Estádio: ${time.strStadium || "não informado"}`,
    `Fundação: ${time.intFormedYear || "não informada"}`,
  ];
  linhas.forEach((texto) => {
    const p = document.createElement("p");
    p.textContent = texto;
    cartao.appendChild(p);
  });

  resultado.appendChild(cartao);
}

document.getElementById("form-time").addEventListener("submit", (evento) => {
  evento.preventDefault(); // evita recarregar a página
  buscarTime(document.getElementById("time").value);
});
