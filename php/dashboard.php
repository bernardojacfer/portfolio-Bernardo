<?php
session_start();

if (empty($_SESSION['usuario_id'])) {
    header('Location: login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Área do Usuário | Meu Projeto Pessoal</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>

  <header class="site-header">
    <div class="brand">Meu Projeto</div>
    <nav>
      <a href="../index.html">Home</a>
      <a href="sobre.html">Sobre</a>
      <a href="contato.html">Contato</a>
      <a href="logout.php">Sair</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Bem-vindo(a), <?= htmlspecialchars($_SESSION['usuario_nome']) ?>!</h1>
      <p class="lead">Você está logado(a). Esta é uma área restrita, visível apenas para quem faz login.</p>
      <a href="logout.php" class="btn">Sair da conta</a>
    </section>
  </main>

  <footer class="site-footer">
    <p>Feito por mim &middot; Colégio UNASP-HT &middot; Técnico em Informática</p>
  </footer>

</body>
</html>
