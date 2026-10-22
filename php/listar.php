<?php

$stmt = $pdo->query(
    'SELECT id, nome, email, criado_em
     FROM usuarios
     ORDER BY id DESC'
);
$usuarios = $stmt->fetchAll();

session_start();

require_once __DIR__ . '/../includes/conexao.php';

if (empty($_SESSION['usuario_id'])) {
    header('Location: login.php');
    exit;
}

$stmt = $pdo->query(
    'SELECT id, nome, email, criado_em
     FROM usuarios
     ORDER BY id DESC'
);

$usuarios = $stmt->fetchAll();
?>

<!DOCTYPE html>

<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

```
<title>Usuários | Meu Projeto</title>

<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/auth.css">
```

</head>

<body>

<header class="site-header">

```
<div class="brand">
    Meu Projeto
</div>

<nav>
    <a href="../index.html">Home</a>
    <a href="sobre.html">Sobre</a>
    <a href="contato.html">Contato</a>
    <a href="dashboard.php">Dashboard</a>
    <a href="logout.php">Sair</a>
</nav>
```

</header>

<main>

```
<section class="hero">

    <h1>Usuários cadastrados</h1>

    <p class="lead">
        Lista de usuários registrados no sistema.
    </p>

    <a href="cadastro.php" class="btn">
        Cadastrar novo usuário
    </a>

    <div class="tabela-container">

        <?php if (empty($usuarios)): ?>

            <p>Nenhum usuário cadastrado.</p>

        <?php else: ?>

            <table>

                <thead>

                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>E-mail</th>
                        <th>Data de cadastro</th>
                        <th>Ações</th>
                    </tr>

                </thead>

                <tbody>

                    <?php foreach ($usuarios as $usuario): ?>

                        <tr>

                            <td>
                                <?= htmlspecialchars($usuario['id']) ?>
                            </td>

                            <td>
                                <?= htmlspecialchars($usuario['nome']) ?>
                            </td>

                            <td>
                                <?= htmlspecialchars($usuario['email']) ?>
                            </td>

                            <td>
                                <?= htmlspecialchars($usuario['criado_em']) ?>
                            </td>

                            <td>

                                <a
                                    href="editar.php?id=<?= $usuario['id'] ?>"
                                    class="btn"
                                >
                                    Editar
                                </a>

                                <form
                                    method="POST"
                                    action="excluir.php"
                                    style="display: inline;"
                                    onsubmit="return confirmarExclusao();"
                                >

                                    <input
                                        type="hidden"
                                        name="id"
                                        value="<?= $usuario['id'] ?>"
                                    >

                                    <button
                                        type="submit"
                                        class="btn btn-excluir"
                                    >
                                        Excluir
                                    </button>

                                </form>

                            </td>

                        </tr>

                    <?php endforeach; ?>

                </tbody>

            </table>

        <?php endif; ?>

    </div>

</section>
```

</main>

<footer class="site-footer">

```
<p>
    Feito por mim &middot;
    Colégio UNASP-HT &middot;
    Técnico em Informática
</p>
```

</footer>

<script>

function confirmarExclusao() {

    return confirm(
        'Tem certeza que deseja excluir este usuário?'
    );

}


</script>

</body>
</html>
