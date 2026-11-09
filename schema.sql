-- Projeto Integrado (DWS + POO + BD) - Etapa 1
-- Modelagem do banco de dados

CREATE DATABASE IF NOT EXISTS meu_projeto
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE meu_projeto;

-- Usuários do sistema (login e CRUD)
CREATE TABLE IF NOT EXISTS usuarios (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nome       VARCHAR(100) NOT NULL,
  email      VARCHAR(150) NOT NULL UNIQUE,
  senha_hash VARCHAR(255) NOT NULL,
  perfil     ENUM('admin', 'comum') NOT NULL DEFAULT 'comum',
  criado_em  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Mensagens enviadas pelo formulário de contato
-- usuario_id é opcional: a mensagem pode vir de alguém sem conta
CREATE TABLE IF NOT EXISTS mensagens (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NULL,
  nome       VARCHAR(100) NOT NULL,
  email      VARCHAR(150) NOT NULL,
  mensagem   TEXT NOT NULL,
  lida       BOOLEAN NOT NULL DEFAULT FALSE,
  criado_em  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_mensagens_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;
