// Mensagens recebidas pelo formulário de contato (read, update e delete).
// Só para administradores. Depende de api.js.

const corpoTabela = document.getElementById("tabela-mensagens");
const aviso = document.getElementById("aviso");
const vazio = document.getElementById("vazio");

async function carregar() {
  const { mensagens } = await api("/api/mensagens");
  corpoTabela.textContent = "";
  vazio.hidden = mensagens.length > 0;
  mensagens.forEach((mensagem) => corpoTabela.appendChild(montarLinha(mensagem)));
}

function montarLinha(mensagem) {
  const linha = document.createElement("tr");
  linha.appendChild(criar("td", formatarData(mensagem.criado_em)));
  linha.appendChild(criar("td", mensagem.nome));
  linha.appendChild(criar("td", mensagem.email));
  linha.appendChild(criar("td", mensagem.mensagem, "msg-texto"));

  const status = document.createElement("td");
  status.appendChild(
    criar("span", mensagem.lida ? "Lida" : "Nova", mensagem.lida ? "badge" : "badge nova")
  );
  linha.appendChild(status);

  const acoes = criar("div", null, "acoes");
  if (!mensagem.lida) {
    const lida = criar("button", "Marcar como lida", "btn btn-pequeno btn-secundario");
    lida.type = "button";
    lida.addEventListener("click", () => marcarLida(mensagem));
    acoes.appendChild(lida);
  }
  const excluir = criar("button", "Excluir", "btn btn-pequeno btn-excluir");
  excluir.type = "button";
  excluir.addEventListener("click", () => excluirMensagem(mensagem));
  acoes.appendChild(excluir);

  const celulaAcoes = document.createElement("td");
  celulaAcoes.appendChild(acoes);
  linha.appendChild(celulaAcoes);
  return linha;
}

async function marcarLida(mensagem) {
  try {
    await api(`/api/mensagens/${mensagem.id}/lida`, { metodo: "PATCH" });
    await carregar();
    mostrarMensagem(aviso, "");
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
}

async function excluirMensagem(mensagem) {
  if (!confirm(`Excluir a mensagem de ${mensagem.nome}?`)) return;
  try {
    await api(`/api/mensagens/${mensagem.id}`, { metodo: "DELETE" });
    await carregar();
    mostrarMensagem(aviso, "Mensagem excluída.", "sucesso");
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
}

(async function iniciar() {
  try {
    const eu = await exigirLogin({ admin: true });
    if (!eu) return;
    await carregar();
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
})();
