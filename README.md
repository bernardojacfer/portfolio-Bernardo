# Portfólio Bernardo — Projeto Integrado (DWS + POO + BD)

Site pessoal com back-end em Python (Flask, programação orientada a objetos) e banco de dados MySQL.
Projeto individual do Colégio UNASP-HT, Técnico em Informática (2º TI).

## Status das etapas

| Etapa | Prazo | Situação |
|---|---|---|
| 1 — Modelagem e banco de dados | 09/11/2026 | Concluída: UML, tabelas e conexão inicial |
| 2 — Back-end (classes, DAOs e rotas Flask) | 13/11/2026 | Em andamento |
| Final — Front-end com Fetch | 17/11/2026 | Pendente |

## Modelo de dados

Diagrama de classes: [docs/diagrama_classes.svg](docs/diagrama_classes.svg)

![Diagrama de classes](docs/diagrama_classes.svg)

| Tabela | Campos |
|---|---|
| `usuarios` | id, nome, email (único), senha_hash, perfil (`admin` ou `comum`), criado_em |
| `mensagens` | id, usuario_id (opcional, chave estrangeira para `usuarios`), nome, email, mensagem, lida, criado_em |

Relacionamento: um usuário pode enviar várias mensagens (0..*), e uma mensagem pode ou não ter usuário (0..1).
Ao excluir um usuário, as mensagens dele ficam no banco com `usuario_id` nulo.

As senhas nunca são guardadas em texto puro: a classe `Usuario` gera e confere o hash (Werkzeug).

## Estrutura do projeto

```
├── app.py                 aplicação Flask (rota /api/saude)
├── config.py              leitura do arquivo .env
├── criar_banco.py         cria o banco e as tabelas a partir do schema.sql
├── testar_conexao.py      confere a conexão e lista as tabelas
├── schema.sql             estrutura do banco de dados
├── models/                classes do domínio (Usuario, Mensagem)
├── dao/                   acesso ao banco (conexao.py; DAOs na Etapa 2)
├── docs/                  diagrama de classes (UML)
├── requirements.txt
└── .env.example           modelo das configurações do banco
```

## Como rodar

Pré-requisitos: Python 3.10+ e MySQL (ou XAMPP) em execução.

```bash
# 1. Ambiente virtual e dependências
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt

# 2. Configuração do banco
copy .env.example .env         # Windows (Linux/Mac: cp .env.example .env)
# edite o .env com o usuário e a senha do seu MySQL

# 3. Criar banco e tabelas
python criar_banco.py

# 4. Testar a conexão
python testar_conexao.py

# 5. Subir o servidor
python app.py
# abra http://127.0.0.1:5000/api/saude
```

Resposta esperada em `/api/saude`: `{"banco": "conectado", "status": "ok"}`.

## Tecnologias

Python, Flask, MySQL, mysql-connector-python, HTML, CSS e JavaScript.
