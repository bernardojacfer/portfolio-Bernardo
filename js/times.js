// Busca informações de um time de futebol na API Flask do projeto (/api/times),
// que consulta a TheSportsDB no servidor, e mostra o resultado sem recarregar a página.
// Se a página estiver aberta em outra porta (ex.: Live Server), chama o Flask na porta 5000.
const API_BASE = window.location.port === "5000" ? "" : "http://127.0.0.1:5000";
const URL_API = `${API_BASE}/api/times`;

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
    const resposta = await fetch(`${URL_API}?nome=${encodeURIComponent(termo)}`);

    let dados = {};
    try {
      dados = await resposta.json();
    } catch (e) {
      // resposta sem JSON: segue com o erro genérico abaixo
    }

    // Cenário inválido 2: a API respondeu com erro (time não encontrado, serviço fora do ar...)
    if (!resposta.ok) {
      resultado.className = "feedback error";
      resultado.textContent =
        dados.erro || `Não foi possível buscar o time (erro ${resposta.status}).`;
      return;
    }

    // Cenário válido: monta o cartão com os dados do JSON
    mostrarTime(dados.time);
  } catch (erro) {
    // Falha de rede: o servidor Flask provavelmente não está rodando
    console.error("Falha na requisição:", erro);
    resultado.className = "feedback error";
    resultado.textContent =
      "Não foi possível falar com o servidor. Confira se o Flask está rodando (python app.py) e tente novamente.";
  }
}

function mostrarTime(time) {
  const resultado = document.getElementById("time-resultado");
  resultado.className = "";
  resultado.innerHTML = "";

  const cartao = document.createElement("div");
  cartao.className = "card time-card";

  if (time.escudo) {
    const img = document.createElement("img");
    img.src = time.escudo;
    img.alt = `Escudo do ${time.nome}`;
    img.className = "time-escudo";
    cartao.appendChild(img);
  }

  const titulo = document.createElement("h2");
  titulo.textContent = time.nome;
  cartao.appendChild(titulo);

  const linhas = [
    `País: ${time.pais || "não informado"}`,
    `Liga: ${time.liga || "não informada"}`,
    `Estádio: ${time.estadio || "não informado"}`,
    `Fundação: ${time.fundacao || "não informada"}`,
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
