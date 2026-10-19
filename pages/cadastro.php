<?php
session_start();
require_once __DIR__ . '/../includes/conexao.php';

$erro = '';
$sucesso = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome  = trim($_POST['nome'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $senha = $_POST['senha'] ?? '';
    $confirmar = $_POST['confirmar_senha'] ?? '';

    if ($nome === '' || $email === '' || $senha === '') {
        $erro = 'Preencha todos os campos.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erro = 'Informe um e-mail válido.';
    } elseif (strlen($senha) < 6) {
        $erro = 'A senha deve ter pelo menos 6 caracteres.';
    } elseif ($senha !== $confirmar) {
        $erro = 'As senhas não coincidem.';
    } else {
        $stmt = $pdo->prepare('SELECT id FROM usuarios WHERE email = :email');
        $stmt->execute([':email' => $email]);

        if ($stmt->fetch()) {
            $erro = 'Este e-mail já está cadastrado.';
        } else {
            $hash = password_hash($senha, PASSWORD_DEFAULT);

            $stmt = $pdo->prepare(
                'INSERT INTO usuarios (nome, email, senha) VALUES (:nome, :email, :senha)'
            );
            $stmt->execute([
                ':nome'  => $nome,
                ':email' => $email,
                ':senha' => $hash,
            ]);

            $sucesso = 'Cadastro realizado com sucesso! Você já pode fazer login.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cadastro | Meu Projeto Pessoal</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>

  <header class="site-header">
    <div class="brand">Meu Projeto</div>
    <nav>
      <a href="../index.html">Home</a>
      <a href="sobre.html">Sobre</a>
      <a href="contato.html">Contato</a>
      <a href="login.php">Login</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Criar conta</h1>

      <?php if ($erro): ?>
        <p class="mensagem erro"><?= htmlspecialchars($erro) ?></p>
      <?php endif; ?>

      <?php if ($sucesso): ?>
        <p class="mensagem sucesso"><?= htmlspecialchars($sucesso) ?></p>
      <?php endif; ?>

      <form method="POST" action="cadastro.php" class="form-auth">
        <label for="nome">Nome</label>
        <input type="text" id="nome" name="nome" required
               value="<?= isset($nome) ? htmlspecialchars($nome) : '' ?>">

        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" required
               value="<?= isset($email) ? htmlspecialchars($email) : '' ?>">

        <label for="senha">Senha</label>
        <input type="password" id="senha" name="senha" required minlength="6">

        <label for="confirmar_senha">Confirmar senha</label>
        <input type="password" id="confirmar_senha" name="confirmar_senha" required minlength="6">

        <button type="submit" class="btn">Cadastrar</button>
      </form>

      <p>Já tem conta? <a href="login.php">Entrar</a></p>
    </section>
  </main>

  <footer class="site-footer">
    <p>Feito por mim &middot; Colégio UNASP-HT &middot; Técnico em Informática</p>
  </footer>

</body>
</html>
