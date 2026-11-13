// Login e cadastro (create). Depende de api.js.

const formLogin = document.getElementById("form-login");
const formCadastro = document.getElementById("form-cadastro");
const aviso = document.getElementById("aviso");

if (formLogin) {
  formLogin.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mostrarMensagem(aviso, "");
    const botao = formLogin.querySelector("button[type=submit]");
    botao.disabled = true;

    try {
      await api("/api/login", {
        metodo: "POST",
        corpo: {
          email: document.getElementById("email").value,
          senha: document.getElementById("senha").value,
        },
      });
      window.location.href = "/pages/dashboard.html";
    } catch (erro) {
      mostrarMensagem(aviso, erro.message, "erro");
      botao.disabled = false;
    }
  });
}

if (formCadastro) {
  formCadastro.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mostrarMensagem(aviso, "");

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;
    const confirmar = document.getElementById("confirmar_senha").value;

    if (!nome || !email || !senha) {
      mostrarMensagem(aviso, "Preencha todos os campos.", "erro");
      return;
    }
    if (senha.length < 6) {
      mostrarMensagem(aviso, "A senha deve ter pelo menos 6 caracteres.", "erro");
      return;
    }
    if (senha !== confirmar) {
      mostrarMensagem(aviso, "As senhas não coincidem.", "erro");
      return;
    }

    const botao = formCadastro.querySelector("button[type=submit]");
    botao.disabled = true;

    try {
      const { usuario } = await api("/api/usuarios", {
        metodo: "POST",
        corpo: { nome, email, senha, confirmar_senha: confirmar },
      });
      const extra = usuario.perfil === "admin"
        ? " Você é o primeiro usuário e foi definido como administrador."
        : "";
      mostrarMensagem(aviso, `Cadastro realizado com sucesso!${extra} Redirecionando para o login...`, "sucesso");
      formCadastro.reset();
      setTimeout(() => { window.location.href = "/pages/login.html"; }, 2000);
    } catch (erro) {
      mostrarMensagem(aviso, erro.message, "erro");
      botao.disabled = false;
    }
  });
}
