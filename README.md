# Projeto: Gerenciador de Tarefas (CRUD Completo com Django)

Este projeto é uma aplicação web completa de "To-Do List" (Gerenciador de Tarefas) desenvolvida em Django.

O projeto cumpre todos os requisitos da disciplina (4 histórias de usuário, banco SQLite), mas foi **elaborado** para incluir um **CRUD Completo** (Create, Read, Update, Delete), uma interface profissional com **Bootstrap** e uma suíte completa de **testes automatizados** para garantir a qualidade do código.

---

## Alunos

* Eduardo Melo - 01706118
* Julia Greicy - 01699517
* Rúbia Evelyn - 01707900
* Italo Guilherme - 01678558

---

## Histórias de Usuário e Funcionalidades

O projeto implementa um CRUD completo, cobrindo 5 histórias de usuário:

1.  **Cadastro (Create):** Como um novo usuário, eu quero me cadastrar na plataforma.
2.  **Login e Leitura (Read):** Como um usuário cadastrado, eu quero fazer login e ver minha lista de tarefas pendentes.
3.  **Criação (Create):** Como um usuário logado, eu quero adicionar uma nova tarefa à minha lista.
4.  **Edição (Update):** Como um usuário logado, eu quero clicar em "Editar" para corrigir o título de uma tarefa existente.
5.  **Gestão (Delete):** Como um usuário logado, eu quero marcar uma tarefa como "concluída" ou "excluir" uma tarefa.

---

## Como Rodar o Projeto

1.  Clone o repositório:
    ```bash
    git clone https://github.com/devm3lo/projeto-django-tarefas
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install django
    ```

4.  Aplique as migrações para criar o banco de dados:
    ```bash
    python manage.py migrate
    ```

5.  Rode o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

---

## Principais URLs do Projeto

Com o servidor rodando, estas são as páginas principais da aplicação:

* **Página Inicial (Lista de Tarefas):** `http://127.0.0.1:8000/`
* **Página de Login:** `http://127.0.0.1:8000/contas/login/`
* **Página de Cadastro:** `http://127.0.0.1:8000/cadastro/`
* **Painel de Admin:** `http://127.0.0.1:8000/admin/`

---

## Testes Automatizados 🧪

Para garantir a qualidade, segurança e estabilidade do código, o projeto foi desenvolvido com uma suíte de **8 testes automatizados** (utilizando o `unittest` do Django).

Os testes validam a lógica de negócio de todo o CRUD (Criar, Ler, Editar, Excluir), incluindo:
* Segurança (bloqueio de usuários não logados).
* Criação, edição, conclusão e exclusão de tarefas.
* Isolamento de dados (um usuário não pode editar/excluir a tarefa de outro).

### Como Rodar os Testes

Para executar a suíte de testes, pare o servidor e rode o seguinte comando:
```bash
python manage.py test