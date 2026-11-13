// Edição de usuário (update). O próprio usuário edita o seu perfil;
// o administrador edita qualquer um e pode mudar o perfil. Depende de api.js.

const formEditar = document.getElementById("form-editar");
const titulo = document.getElementById("titulo");
const aviso = document.getElementById("aviso");
const campoPerfil = document.getElementById("campo-perfil");

(async function iniciar() {
  try {
    const eu = await exigirLogin();
    if (!eu) return;

    const id = Number(new URLSearchParams(window.location.search).get("id")) || eu.id;
    const { usuario } = await api(`/api/usuarios/${id}`);
    const proprio = usuario.id === eu.id;

    titulo.textContent = proprio ? "Editar meu perfil" : `Editar ${usuario.nome}`;
    document.getElementById("nome").value = usuario.nome;
    document.getElementById("email").value = usuario.email;

    // Só o admin muda o perfil de outras pessoas (nunca o próprio).
    const podeMudarPerfil = eu.perfil === "admin" && !proprio;
    campoPerfil.hidden = !podeMudarPerfil;
    document.getElementById("perfil").value = usuario.perfil;

    document.getElementById("link-voltar").href =
      eu.perfil === "admin" ? "usuarios.html" : "dashboard.html";
    formEditar.hidden = false;

    formEditar.addEventListener("submit", async (evento) => {
      evento.preventDefault();
      mostrarMensagem(aviso, "");

      const corpo = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value, // vazio = manter a senha atual
      };
      if (podeMudarPerfil) corpo.perfil = document.getElementById("perfil").value;

      const botao = formEditar.querySelector("button[type=submit]");
      botao.disabled = true;
      try {
        const { usuario: salvo } = await api(`/api/usuarios/${id}`, { metodo: "PUT", corpo });
        titulo.textContent = proprio ? "Editar meu perfil" : `Editar ${salvo.nome}`;
        document.getElementById("senha").value = "";
        mostrarMensagem(aviso, "Alterações salvas com sucesso.", "sucesso");
      } catch (erro) {
        mostrarMensagem(aviso, erro.message, "erro");
      } finally {
        botao.disabled = false;
      }
    });
  } catch (erro) {
    mostrarMensagem(aviso, erro.message, "erro");
  }
})();
