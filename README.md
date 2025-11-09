# Projeto: Gerenciador de Tarefas (Django)

O objetivo é uma aplicação web simples de "To-Do List" usando o framework Django, atendendo aos requisitos mínimos de 4 histórias de usuário e persistência de dados em um banco SQLite.

---

## Alunos

* Eduardo Melo - 01706118
* Julia Greicy - 01699517
* Rúbia Evelyn - 01707900
* Italo Guilherme - 01678558

---

## Histórias de Usuário Implementadas

O projeto implementa as seguintes 4 histórias de usuário:

1.  **Cadastro de Usuário:** Como um novo usuário, eu quero me cadastrar na plataforma, para que eu possa ter minha própria conta.
2.  **Autenticação e Listagem:** Como um usuário cadastrado, eu quero fazer login e ver minha lista de tarefas pendentes, para que eu saiba o que preciso fazer.
3.  **Criação de Tarefa:** Como um usuário logado, eu quero adicionar uma nova tarefa à minha lista (informando um título), para que eu possa registrar novos itens.
4.  **Gerenciamento de Tarefas:** Como um usuário logado, eu quero marcar uma tarefa como "concluída" ou "excluir" uma tarefa, para que eu possa gerenciar minha lista.

---

## Como Rodar o Projeto

Para rodar este projeto localmente, siga os passos:

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

---

## Acessando o Painel de Admin

O projeto também inclui o painel de administração padrão do Django, onde é possível gerenciar usuários e tarefas diretamente pelo banco de dados.

1.  Para acessá-lo, primeiro crie um superusuário:
    ```bash
    python manage.py createsuperuser
    ```
    (Siga os prompts para criar seu usuário e senha de admin)

2.  Com o servidor rodando, acesse `http://127.0.0.1:8000/admin/`

3.  Faça login com os dados do superusuário que você acabou de criar.