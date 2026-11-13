// Lista de usuários (read), com busca e exclusão (delete). Só para administradores.
// Depende de api.js.

const corpoTabela = document.getElementById("tabela-usuarios");
const aviso = document.getElementById("aviso");
const vazio = document.getElementById("vazio");
const campoBusca = document.getElementById("busca");
let eu = null;

async function carregar() {
  const busca = campoBusca.value.trim();
  const url = busca ? `/api/usuarios?busca=${encodeURIComponent(busca)}` : "/api/usuarios";
  const { usuarios } = await api(url);

  corpoTabela.textContent = "";
  vazio.hidden = usuarios.length > 0;
  usuarios.forEach((usuario) => corpoTabela.appendChild(montarLinha(usuario)));
}

function montarLinha(usuario) {
  const linha = document.createElement("tr");
  linha.appendChild(criar("td", usuario.id));
  linha.appendChild(criar("td", usuario.nome));
  linha.appendChild(criar("td", usuario.email));

  const perfil = document.createElement("td");
  const admin = usuario.perfil === "admin";
  perfil.appendChild(criar("span", admin ? "Admin" : "Comum", admin ? "badge admin" : "badge"));
  linha.appendChild(perfil);

  linha.appendChild(criar("td", formatarData(usuario.criado_em)));

  const acoes = criar("div", null, "acoes");
  const editar = criar("a", "Editar", "btn btn-pequeno btn-secundario");
  editar.href = `editar.html?id=${usuario.id}`;
  acoes.appendChild(editar);

  if (usuario.id === eu.id) {
    acoes.appendChild(criar("span", "Você", "badge"));
  } else {
    const excluir = criar("button", "Excluir", "btn btn-pequeno btn-excluir");
    excluir.type = "button";
    excluir.addEventListener("click", () => excluirUsuario(usuario));
    acoes.appendChild(excluir);
  }

  const celulaAcoes = document.createElement("td");
  celulaAcoes.appendChild(acoes);
  linha.appendChild(celulaAcoes);
  return linha;
}

async function excluirUsuario(usuario) {
  if (!confirm(`Tem certeza que deseja excluir ${usuario.nome}?`)) return;
  try {
    await api(`/api/usuarios/${usuario.id}`, { metodo: "DELETE" });
    await carregar();
    mostrarMensagem(aviso, `Usuário ${usuario.nome} excluído.`, "sucesso");
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
}

document.getElementById("form-busca").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mostrarMensagem(aviso, "");
  try {
    await carregar();
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
});

(async function iniciar() {
  try {
    eu = await exigirLogin({ admin: true });
    if (!eu) return;
    await carregar();
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
})();
