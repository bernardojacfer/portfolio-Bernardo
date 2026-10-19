<?php
session_start();
require_once __DIR__ . '/../includes/conexao.php';

if (empty($_SESSION['usuario_id'])) {
    header('Location: login.php');
    exit;
}

$erro = '';
$id = $_GET['id'] ?? $_POST['id'] ?? null;

if (!$id) {
    header('Location: listar.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome  = trim($_POST['nome'] ?? '');
    $email = trim($_POST['email'] ?? '');

    if ($nome === '' || $email === '') {
        $erro = 'Preencha todos os campos.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erro = 'Informe um e-mail válido.';
    } else {
        // UPDATE ... SET — Seção 6.3 da apostila
        $stmt = $pdo->prepare('UPDATE usuarios SET nome = :nome, email = :email WHERE id = :id');
        $stmt->execute([
            ':nome'  => $nome,
            ':email' => $email,
            ':id'    => $id,
        ]);
        header('Location: listar.php');
        exit;
    }
}

// SELECT com prepared statement — Seção 6.2/6.4
$stmt = $pdo->prepare('SELECT id, nome, email FROM usuarios WHERE id = :id');
$stmt->execute([':id' => $id]);
$usuario = $stmt->fetch();

if (!$usuario) {
    header('Location: listar.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Editar usuário | Meu Projeto Pessoal</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/auth.css">
</head>
<body>

  <header class="site-header">
    <div class="brand">Meu Projeto</div>
    <nav>
      <a href="../index.html">Home</a>
      <a href="sobre.html">Sobre</a>
      <a href="contato.html">Contato</a>
      <a href="listar.php">Usuários</a>
      <a href="logout.php">Sair</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Editar usuário</h1>

      <?php if ($erro): ?>
        <p class="mensagem erro"><?= htmlspecialchars($erro) ?></p>
      <?php endif; ?>

      <form method="POST" action="editar.php" class="form-auth">
        <input type="hidden" name="id" value="<?= $usuario['id'] ?>">

        <label for="nome">Nome</label>
        <input type="text" id="nome" name="nome" required
               value="<?= htmlspecialchars($usuario['nome']) ?>">

        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" required
               value="<?= htmlspecialchars($usuario['email']) ?>">

        <button type="submit" class="btn">Salvar alterações</button>
      </form>

      <p><a href="listar.php">← Voltar para a lista</a></p>
    </section>
  </main>

  <footer class="site-footer">
    <p>Feito por mim &middot; Colégio UNASP-HT &middot; Técnico em Informática</p>
  </footer>

</body>
</html>