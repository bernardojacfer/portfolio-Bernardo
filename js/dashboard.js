// Área do usuário. Depende de api.js.

const titulo = document.getElementById("titulo");
const subtitulo = document.getElementById("subtitulo");
const aviso = document.getElementById("aviso");

(async function iniciar() {
  try {
    const usuario = await exigirLogin();
    if (!usuario) return;

    titulo.textContent = `Bem-vindo(a), ${usuario.nome}!`;
    subtitulo.textContent =
      usuario.perfil === "admin"
        ? "Você está logado como administrador."
        : "Você está logado(a). Esta é uma área restrita, visível apenas para quem faz login.";

    const linkPerfil = document.getElementById("link-perfil");
    linkPerfil.href = `editar.html?id=${usuario.id}`;
    linkPerfil.hidden = false;

    if (usuario.perfil !== "admin") return;

    document.getElementById("link-usuarios").hidden = false;
    document.getElementById("link-mensagens").hidden = false;

    // Resumo para o administrador
    const [{ usuarios }, { mensagens }] = await Promise.all([
      api("/api/usuarios"),
      api("/api/mensagens"),
    ]);
    const naoLidas = mensagens.filter((m) => !m.lida).length;
    const resumo = document.getElementById("resumo");
    resumo.textContent =
      `${usuarios.length} usuário(s) cadastrado(s) · ${naoLidas} mensagem(ns) não lida(s)`;
    resumo.hidden = false;
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
})();
