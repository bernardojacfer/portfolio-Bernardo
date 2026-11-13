// Completa o menu do topo conforme o estado de login:
//   visitante -> Login e Cadastro
//   logado    -> Dashboard, (Usuários e Mensagens para admin) e Sair
(async function montarMenu() {
  const nav = document.querySelector(".site-header nav");
  if (!nav) return;

  function adicionar(texto, href) {
    const link = document.createElement("a");
    link.textContent = texto;
    link.href = href;
    if (link.pathname === window.location.pathname) link.classList.add("active");
    nav.appendChild(link);
    return link;
  }

  let usuario = null;
  try {
    const resposta = await fetch("/api/me", { credentials: "same-origin" });
    if (resposta.ok) usuario = (await resposta.json()).usuario;
  } catch (e) {
    // servidor fora do ar: mostra o menu de visitante
  }

  if (!usuario) {
    adicionar("Login", "/pages/login.html");
    adicionar("Cadastro", "/pages/cadastro.html");
    return;
  }

  adicionar("Dashboard", "/pages/dashboard.html");
  if (usuario.perfil === "admin") {
    adicionar("Usuários", "/pages/usuarios.html");
    adicionar("Mensagens", "/pages/mensagens.html");
  }

  const sair = adicionar("Sair", "#");
  sair.addEventListener("click", async (evento) => {
    evento.preventDefault();
    try {
      await fetch("/api/logout", { method: "POST", credentials: "same-origin" });
    } finally {
      window.location.href = "/pages/login.html";
    }
  });
})();
